from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['is_superuser'] = user.is_superuser
        return token



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Password is accepted but not displayed

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'].lower(),# Normalize email to lowercase
            username=validated_data.get('username', ''),
        )
        user.set_password(validated_data['password'])  # Securely hash the password
        user.save()
        return user
