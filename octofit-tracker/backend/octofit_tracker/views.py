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
    # Avoid prefetching related managers when ObjectId PKs can be unset on
    # model instances returned by djongo; counts are computed in the serializer.
    queryset = Team.objects.all().order_by('name')
    serializer_class = TeamSerializer

class WorkoutViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for workouts."""
    # Avoid prefetching M2M relations that may access a missing PK; serializer
    # handles suggested_for counts defensively instead.
    queryset = Workout.objects.all().order_by('name')
    serializer_class = WorkoutSerializer

class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for leaderboard entries."""
    queryset = Leaderboard.objects.select_related('user').all().order_by('rank')
    serializer_class = LeaderboardSerializer
