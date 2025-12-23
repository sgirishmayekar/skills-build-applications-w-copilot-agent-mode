from rest_framework import viewsets
from .models import Activity, User, Team, Workout, Leaderboard
from .serializers import (
    ActivitySerializer, UserSerializer, TeamSerializer,
    WorkoutSerializer, LeaderboardSerializer,
)

class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for activities."""
    queryset = Activity.objects.select_related('user').all().order_by('-date')
    serializer_class = ActivitySerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for users."""
    queryset = User.objects.select_related('team').all().order_by('name')
    serializer_class = UserSerializer

class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for teams."""
    queryset = Team.objects.prefetch_related('members').all().order_by('name')
    serializer_class = TeamSerializer

class WorkoutViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for workouts."""
    queryset = Workout.objects.prefetch_related('suggested_for').all().order_by('name')
    serializer_class = WorkoutSerializer

class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for leaderboard entries."""
    queryset = Leaderboard.objects.select_related('user').all().order_by('rank')
    serializer_class = LeaderboardSerializer
