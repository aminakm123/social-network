from django.urls import path
from .views import register_user, MyTokenObtainPairView, search_users, send_friend_request, accept_friend_request, reject_friend_request, list_friends, list_pending_requests
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "user"

urlpatterns = [
    path('register/', register_user, name='register'),
    path('', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('search/', search_users, name='search_users'),
    path('friend-request/send/<int:to_user_id>/', send_friend_request, name='send_friend_request'),
    path('friend-request/accept/<int:friend_request_id>/', accept_friend_request, name='accept_friend_request'),
    path('friend-request/reject/<int:friend_request_id>/', reject_friend_request, name='reject_friend_request'),
    path('friends/', list_friends, name='list_friends'),
    path('pending-requests/', list_pending_requests, name='list_pending_requests')
]
