from django.test import TestCase
from rest_framework.test import APIClient
from octofit_tracker.models import Team, User, Activity
import datetime

class ActivitiesAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        team = Team.objects.create(name='Test', description='t')
        user = User.objects.create(name='A', email='a@a.com', team=team)
        Activity.objects.create(user=user, activity_type='Run', duration=30, date=datetime.date.today())

    def test_list_activities(self):
        res = self.client.get('/api/activities/')
        self.assertIn(res.status_code, (200, 302))
        data = res.json()
        # Accept both paginated and list responses
        items = data if isinstance(data, list) else data.get('results', [])
        self.assertTrue(isinstance(items, list))
        self.assertGreaterEqual(len(items), 1)
        self.assertIn('activity_type', items[0])
