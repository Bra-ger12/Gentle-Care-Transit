from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Driver(models.Model):
    """
    Driver profile model.
    """
    AVAILABILITY_CHOICES = (
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('on_trip', 'On Trip'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver')
    full_name = models.CharField(max_length=255)
    license_number = models.CharField(max_length=50, unique=True)
    license_expiry = models.DateField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    total_trips = models.IntegerField(default=0)
    availability_status = models.CharField(
        max_length=20, choices=AVAILABILITY_CHOICES, default='offline'
    )
    current_location_lat = models.DecimalField(
        max_digits=10, decimal_places=8, null=True, blank=True
    )
    current_location_lng = models.DecimalField(
        max_digits=11, decimal_places=8, null=True, blank=True
    )
    last_location_update = models.DateTimeField(null=True, blank=True)
    background_check_status = models.CharField(
        max_length=20, default='pending', choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ]
    )
    document_url = models.URLField(null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['license_number']),
            models.Index(fields=['availability_status']),
        ]
    
    def __str__(self):
        return self.full_name
