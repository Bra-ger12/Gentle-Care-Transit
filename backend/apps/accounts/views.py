from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    UserSerializer, RegisterSerializer, OTPVerificationSerializer, LoginSerializer
)

User = get_user_model()

class AuthViewSet(viewsets.ViewSet):
    """
    API endpoint for user authentication.
    """
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """
        Register a new user.
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    'message': 'User registered successfully. Check email for OTP.',
                    'user_id': str(user.id),
                    'email': user.email
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def verify_otp(self, request):
        """
        Verify OTP and activate user account.
        """
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.validated_data['email'])
                
                # Check if OTP is expired
                if timezone.now() > user.otp_expires_at:
                    return Response(
                        {'error': 'OTP has expired.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Check if OTP is correct
                if user.otp_code != serializer.validated_data['otp_code']:
                    return Response(
                        {'error': 'Invalid OTP.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Mark user as verified
                user.is_verified = True
                user.is_active = True
                user.otp_code = None
                user.save()
                
                return Response(
                    {'message': 'OTP verified successfully. Account activated.'},
                    status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                return Response(
                    {'error': 'User not found.'},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        User login with email and password.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            
            if user is None:
                return Response(
                    {'error': 'Invalid credentials.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            if not user.is_verified:
                return Response(
                    {'error': 'Account not verified. Please verify your OTP.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Update last login
            user.last_login = timezone.now()
            user.save()
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
