from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import random

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    class Meta:
        model = User
        fields = [
            'id', 'email', 'phone', 'first_name', 'last_name',
            'role', 'is_verified', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['email', 'phone', 'password', 'password2', 'role']
    
    def validate(self, data):
        if data['password'] != data.pop('password2'):
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        # Generate and send OTP
        user.otp_code = ''.join(random.choices('0123456789', k=6))
        user.otp_expires_at = timezone.now() + timedelta(minutes=10)
        user.save()
        return user

class OTPVerificationSerializer(serializers.Serializer):
    """
    Serializer for OTP verification.
    """
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
