from rest_framework import viewsets, permissions
from .models import Driver
from .serializers import DriverSerializer

class DriverViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Driver model.
    """
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter drivers by current user.
        """
        if self.request.user.role == 'admin':
            return Driver.objects.all()
        if hasattr(self.request.user, 'driver'):
            return Driver.objects.filter(user=self.request.user)
        return Driver.objects.none()
