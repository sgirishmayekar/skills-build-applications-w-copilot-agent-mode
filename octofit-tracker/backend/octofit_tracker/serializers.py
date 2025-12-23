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
    members_count = serializers.SerializerMethodField()

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

    def get_members_count(self, obj):
        # Try to use the related manager if the instance has a usable PK
        try:
            return obj.members.count()
        except ValueError:
            # Fallback: query MongoDB directly by team name
            try:
                import pymongo
                from django.conf import settings
                db_name = settings.DATABASES['default'].get('NAME', 'octofit_db')
                host = settings.DATABASES['default'].get('CLIENT', {}).get('host', 'localhost')
                port = settings.DATABASES['default'].get('CLIENT', {}).get('port', 27017)
                client = pymongo.MongoClient(host=host, port=port)
                db = client[db_name]
                team_doc = db['teams'].find_one({'name': obj.name})
                if not team_doc:
                    return 0
                return db['users'].count_documents({'team_id': team_doc['_id']})
            except Exception:
                return 0

class WorkoutSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    suggested_for_count = serializers.SerializerMethodField()

    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'suggested_for_count']

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
            doc = db['workouts'].find_one({'name': obj.name})
            if doc and '_id' in doc:
                return str(doc['_id'])
        except Exception:
            pass
        return None

    def get_suggested_for_count(self, obj):
        try:
            return obj.suggested_for.count()
        except ValueError:
            # If the related manager cannot be used (missing PK), fall back to 0
            try:
                # Some djongo configs store M2M in separate collections; attempt to count via MongoDB if present
                import pymongo
                from django.conf import settings
                db_name = settings.DATABASES['default'].get('NAME', 'octofit_db')
                host = settings.DATABASES['default'].get('CLIENT', {}).get('host', 'localhost')
                port = settings.DATABASES['default'].get('CLIENT', {}).get('port', 27017)
                client = pymongo.MongoClient(host=host, port=port)
                db = client[db_name]
                # Try to find a through collection pattern or embedded field; conservatively return 0 if unknown
                return 0
            except Exception:
                return 0

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
