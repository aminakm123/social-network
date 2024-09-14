from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta
from .models import User, FriendRequest
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from user.serializers import MyTokenObtainPairSerializer, UserSerializer, RegisterSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.response import Response




# Max limit for friend requests within one minute
FRIEND_REQUEST_LIMIT = 3
RATE_LIMIT_DURATION = 60  # 60 seconds (1 minute)

# Pagination class
class UserPagination(PageNumberPagination):
    page_size = 10


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # User creation logic in serializer
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API to search users by email or name (with pagination)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users(request):
    search_keyword = request.GET.get('q', '').strip()

    if not search_keyword:
        return Response({'error': 'Search keyword is required.'}, status=status.HTTP_400_BAD_REQUEST)
    users = User.objects.all()
    print(users)
    # Exact email match
    if '@' in search_keyword:
        user = User.objects.filter(email__iexact=search_keyword)
    else:
        # Partial name match
        user = User.objects.filter(username__icontains=search_keyword)

    paginator = UserPagination()
    result_page = paginator.paginate_queryset(user, request)
    serializer = UserSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


# API to accept friend request
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request, friend_request_id):
    friend_request = get_object_or_404(FriendRequest, id=friend_request_id, to_user=request.user)

    if friend_request.accepted:
        return Response({'error': 'Friend request is already accepted.'}, status=status.HTTP_400_BAD_REQUEST)

    friend_request.accepted = True
    friend_request.save()

    return Response({'message': 'Friend request accepted successfully.'}, status=status.HTTP_200_OK)


# API to reject friend request
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_friend_request(request, friend_request_id):
    friend_request = get_object_or_404(FriendRequest, id=friend_request_id, to_user=request.user)

    if friend_request.accepted:
        return Response({'error': 'Cannot reject an already accepted friend request.'}, status=status.HTTP_400_BAD_REQUEST)

    friend_request.delete()
    return Response({'message': 'Friend request rejected successfully.'}, status=status.HTTP_200_OK)


# API to list friends (users who have accepted the friend request)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_friends(request):
    # Get users who have accepted the friend request from either side
    friends = User.objects.filter(
        Q(friend_requests_sent__accepted=True, friend_requests_sent__to_user=request.user) |
        Q(friend_requests_received__accepted=True, friend_requests_received__from_user=request.user)
    )
    
    serializer = UserSerializer(friends, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# API to list pending friend requests (received but not accepted yet)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_pending_requests(request):
    pending_requests = FriendRequest.objects.filter(to_user=request.user, accepted=False)
    
    data = [{
        'id': req.id,
        'from_user': UserSerializer(req.from_user).data,
        'created_at': req.created_at
    } for req in pending_requests]

    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def send_friend_request(request, to_user_id):
    from_user = request.user
    to_user = User.objects.get(id=to_user_id)
    
    # Get the current time and time 1 minute ago
    current_time = timezone.now()
    one_minute_ago = current_time - timedelta(seconds=RATE_LIMIT_DURATION)
    
    # Count the friend requests sent by the user within the last minute
    request_count = FriendRequest.objects.filter(
        from_user=from_user,
        created_at__gte=one_minute_ago
    ).count()

    # Check if the user has exceeded the rate limit
    if request_count >= FRIEND_REQUEST_LIMIT:
        return JsonResponse(
            {'error': 'Friend request limit reached. Try again after some time.'},
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )

    # Check if a friend request already exists between these users
    if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
        return JsonResponse(
            {'error': 'Friend request already sent.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create the friend request
    friend_request = FriendRequest.objects.create(from_user=from_user, to_user=to_user)

    return JsonResponse(
        {'message': 'Friend request sent successfully.'},
        status=status.HTTP_201_CREATED
    )
