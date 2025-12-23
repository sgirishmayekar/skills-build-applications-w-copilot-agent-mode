from rest_framework import serializers
from .models import Activity, User, Team, Workout, Leaderboard

class ActivitySerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Activity
        fields = ['id', 'user_id', 'user_name', 'activity_type', 'duration', 'date']

    def get_id(self, obj):
        # Prefer instance id; fall back to querying the MongoDB document
        try:
            if getattr(obj, 'id', None):
                return str(obj.id)
        except Exception:
            pass
        try:
            import pymongo
            from django.conf import settings
            db_name = settings.DATABASES['default'].get('NAME', 'octofit_db')
            host = settings.DATABASES['default'].get('CLIENT', {}).get('host', 'localhost')
            port = settings.DATABASES['default'].get('CLIENT', {}).get('port', 27017)
            client = pymongo.MongoClient(host=host, port=port)
            db = client[db_name]
            doc = db['activities'].find_one({'activity_type': obj.activity_type, 'date': obj.date})
            if doc and '_id' in doc:
                return str(doc['_id'])
        except Exception:
            pass
        return None

    def get_user_id(self, obj):
        try:
            if obj.user and getattr(obj.user, 'id', None):
                return str(obj.user.id)
        except Exception:
            pass
        return None

class UserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    team_id = serializers.SerializerMethodField()
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'team_id', 'team_name']

    def get_id(self, obj):
        try:
            if getattr(obj, 'id', None):
                return str(obj.id)
        except Exception:
            pass
        try:
            import pymongo
            from django.conf import settings
            db_name = settings.DATABASES['default'].get('NAME', 'octofit_db')
            host = settings.DATABASES['default'].get('CLIENT', {}).get('host', 'localhost')
            port = settings.DATABASES['default'].get('CLIENT', {}).get('port', 27017)
            client = pymongo.MongoClient(host=host, port=port)
            db = client[db_name]
            doc = db['users'].find_one({'email': obj.email})
            if doc and '_id' in doc:
                return str(doc['_id'])
        except Exception:
            pass
        return None

    def get_team_id(self, obj):
        try:
            if obj.team and getattr(obj.team, 'id', None):
                return str(obj.team.id)
        except Exception:
            pass
        try:
            import pymongo
            from django.conf import settings
            db_name = settings.DATABASES['default'].get('NAME', 'octofit_db')
            host = settings.DATABASES['default'].get('CLIENT', {}).get('host', 'localhost')
            port = settings.DATABASES['default'].get('CLIENT', {}).get('port', 27017)
            client = pymongo.MongoClient(host=host, port=port)
            db = client[db_name]
            if obj.team:
                doc = db['teams'].find_one({'name': obj.team.name})
                if doc and '_id' in doc:
                    return str(doc['_id'])
        except Exception:
            pass
        return None

class TeamSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    members_count = serializers.IntegerField(source='members.count', read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'members_count']

    def get_id(self, obj):
        try:
            if getattr(obj, 'id', None):
                return str(obj.id)
        except Exception:
            pass
        try:
            import pymongo
            from django.conf import settings
            db_name = settings.DATABASES['default'].get('NAME', 'octofit_db')
            host = settings.DATABASES['default'].get('CLIENT', {}).get('host', 'localhost')
            port = settings.DATABASES['default'].get('CLIENT', {}).get('port', 27017)
            client = pymongo.MongoClient(host=host, port=port)
            db = client[db_name]
            doc = db['teams'].find_one({'name': obj.name})
            if doc and '_id' in doc:
                return str(doc['_id'])
        except Exception:
            pass
        return None

class WorkoutSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    suggested_for_count = serializers.IntegerField(source='suggested_for.count', read_only=True)

    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'suggested_for_count']

    def get_id(self, obj):
        return str(obj.id)

class LeaderboardSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Leaderboard
        fields = ['id', 'user_id', 'user_name', 'score', 'rank']

    def get_id(self, obj):
        return str(obj.id)

    def get_user_id(self, obj):
        return str(obj.user.id) if obj.user else None
