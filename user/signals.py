# signals.py
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import User, FriendRequest

@receiver(post_delete, sender=User)
def delete_friend_requests(sender, instance, **kwargs):
    # Delete all friend requests where this user is the sender or receiver
    FriendRequest.objects.filter(from_user=instance).delete()
    FriendRequest.objects.filter(to_user=instance).delete()
