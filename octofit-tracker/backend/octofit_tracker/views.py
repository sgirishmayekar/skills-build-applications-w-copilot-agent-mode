from rest_framework import viewsets
from .models import Activity
from .serializers import ActivitySerializer

class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for activities."""
    queryset = Activity.objects.select_related('user').all().order_by('-date')
    serializer_class = ActivitySerializer
