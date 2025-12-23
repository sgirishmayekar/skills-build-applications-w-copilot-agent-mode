from django.core.management.base import BaseCommand
from octofit_tracker.models import Team, User, Activity, Workout, Leaderboard
import datetime

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write('Deleting existing data...')
        # Attempt standard deletions; if that fails (e.g., inconsistent ObjectIds),
        # fall back to dropping MongoDB collections directly to ensure a clean state.
        try:
            Leaderboard.objects.all().delete()
            Activity.objects.all().delete()
            Workout.objects.all().delete()
            User.objects.all().delete()
            Team.objects.all().delete()
        except Exception as e:
            self.stdout.write(f'Warning: standard delete failed: {e}. Falling back to dropping collections via pymongo.')
            try:
                import pymongo
                from django.conf import settings
                db_name = settings.DATABASES['default'].get('NAME', 'octofit_db')
                host = settings.DATABASES['default'].get('CLIENT', {}).get('host', 'localhost')
                port = settings.DATABASES['default'].get('CLIENT', {}).get('port', 27017)
                client = pymongo.MongoClient(host=host, port=port)
                db = client[db_name]
                for coll in ['leaderboard', 'activities', 'workouts', 'users', 'teams']:
                    try:
                        db.drop_collection(coll)
                        self.stdout.write(f'Dropped collection: {coll}')
                    except Exception as e2:
                        self.stdout.write(f'Failed to drop collection {coll}: {e2}')
            except Exception as e3:
                self.stdout.write(f'Failed to fallback drop collections: {e3}')

        self.stdout.write('Creating teams...')
        # Let djongo create ObjectId primary keys automatically
        marvel = Team.objects.create(name='Marvel', description='Marvel heroes')
        dc = Team.objects.create(name='DC', description='DC heroes')

        self.stdout.write('Creating users...')
        # Create users linked to teams; primary keys will be ObjectIds
        tony = User.objects.create(name='Tony Stark', email='tony@stark.com', team=marvel)
        steve = User.objects.create(name='Steve Rogers', email='steve@rogers.com', team=marvel)
        bruce = User.objects.create(name='Bruce Wayne', email='bruce@wayne.com', team=dc)
        clark = User.objects.create(name='Clark Kent', email='clark@kent.com', team=dc)

        self.stdout.write('Creating activities...')
        today = datetime.date.today()
        Activity.objects.create(user=tony, activity_type='Running', duration=30, date=today)
        Activity.objects.create(user=steve, activity_type='Cycling', duration=45, date=today)
        Activity.objects.create(user=bruce, activity_type='Swimming', duration=60, date=today)
        Activity.objects.create(user=clark, activity_type='Yoga', duration=20, date=today)

        self.stdout.write('Creating workouts...')
        w1 = Workout.objects.create(name='HIIT Blast', description='High intensity interval training')
        try:
            w1.suggested_for.add(tony)
            w1.suggested_for.add(steve)
        except Exception as e:
            self.stdout.write(f'Warning: could not add suggested_for for HIIT Blast: {e}')

        w2 = Workout.objects.create(name='Calm Stretch', description='Stretching and mobility')
        try:
            w2.suggested_for.add(bruce)
            w2.suggested_for.add(clark)
        except Exception as e:
            self.stdout.write(f'Warning: could not add suggested_for for Calm Stretch: {e}')

        self.stdout.write('Creating leaderboard entries...')
        Leaderboard.objects.create(user=tony, score=1000, rank=1)
        Leaderboard.objects.create(user=steve, score=900, rank=2)
        Leaderboard.objects.create(user=clark, score=800, rank=3)
        Leaderboard.objects.create(user=bruce, score=700, rank=4)

        self.stdout.write(self.style.SUCCESS('Database populated with test data.'))
