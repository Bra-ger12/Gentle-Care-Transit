from django.contrib import admin
from .models import Vehicle

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('plate_number', 'make', 'model', 'vehicle_type', 'driver', 'is_active', 'created_at')
    list_filter = ('vehicle_type', 'is_active', 'created_at')
    search_fields = ('plate_number', 'make', 'model', 'driver__full_name')
    readonly_fields = ('id', 'created_at', 'updated_at')
