from rest_framework import viewsets, permissions
from .models import Patient
from .serializers import PatientSerializer

class PatientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Patient model.
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter patients by current user.
        """
        if self.request.user.role == 'admin':
            return Patient.objects.all()
        if hasattr(self.request.user, 'patient'):
            return Patient.objects.filter(user=self.request.user)
        return Patient.objects.none()
