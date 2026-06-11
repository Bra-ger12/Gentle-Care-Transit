from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'date_of_birth', 'verified_at', 'created_at')
    list_filter = ('verified_at', 'created_at')
    search_fields = ('full_name', 'user__email')
    readonly_fields = ('id', 'created_at', 'updated_at')
