from rest_framework import serializers
from .models import Activity, User, Team, Workout, Leaderboard

class ActivitySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Activity
        fields = ['id', 'user', 'user_name', 'activity_type', 'duration', 'date']

class UserSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'team', 'team_name']

class TeamSerializer(serializers.ModelSerializer):
    members_count = serializers.IntegerField(source='members.count', read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'members_count']

class WorkoutSerializer(serializers.ModelSerializer):
    suggested_for_count = serializers.IntegerField(source='suggested_for.count', read_only=True)

    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'suggested_for_count']

class LeaderboardSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Leaderboard
        fields = ['id', 'user', 'user_name', 'score', 'rank']
