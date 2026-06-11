from django.contrib import admin
from .models import Driver

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'license_number', 'rating', 'availability_status', 'background_check_status', 'created_at')
    list_filter = ('availability_status', 'background_check_status', 'created_at')
    search_fields = ('full_name', 'license_number', 'user__email')
    readonly_fields = ('id', 'created_at', 'updated_at')
