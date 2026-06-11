from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient model.
    """
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_phone = serializers.CharField(source='user.phone', read_only=True)
    
    class Meta:
        model = Patient
        fields = [
            'id', 'user_email', 'user_phone', 'full_name', 'date_of_birth',
            'blood_type', 'allergies', 'medical_notes', 'special_needs',
            'emergency_contact_name', 'emergency_contact_phone', 'verified_at', 'created_at'
        ]
        read_only_fields = ['id', 'verified_at', 'created_at']
