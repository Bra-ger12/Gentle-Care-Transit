from rest_framework import serializers
from .models import Driver

class DriverSerializer(serializers.ModelSerializer):
    """
    Serializer for Driver model.
    """
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_phone = serializers.CharField(source='user.phone', read_only=True)
    
    class Meta:
        model = Driver
        fields = [
            'id', 'user_email', 'user_phone', 'full_name', 'license_number',
            'license_expiry', 'date_of_birth', 'rating', 'total_trips',
            'availability_status', 'current_location_lat', 'current_location_lng',
            'background_check_status', 'verified_at', 'created_at'
        ]
        read_only_fields = ['id', 'rating', 'total_trips', 'verified_at', 'created_at']
