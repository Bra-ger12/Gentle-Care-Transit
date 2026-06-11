from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Patient(models.Model):
    """
    Patient profile model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient')
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    blood_type = models.CharField(max_length=10, null=True, blank=True)
    allergies = models.TextField(null=True, blank=True)
    medical_notes = models.TextField(null=True, blank=True)
    special_needs = models.TextField(null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=255, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['full_name']),
        ]
    
    def __str__(self):
        return self.full_name
