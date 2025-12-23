from django.test import TestCase
from rest_framework.test import APIClient
from octofit_tracker.models import Team, User, Workout, Leaderboard
import datetime

class OtherAPIsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        t = Team.objects.create(name='X', description='x')
        u = User.objects.create(name='U', email='u@u.com', team=t)
        Workout.objects.create(name='TestW', description='w')
        Leaderboard.objects.create(user=u, score=10, rank=1)

    def test_users(self):
        res = self.client.get('/api/users/')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        items = data if isinstance(data, list) else data.get('results', [])
        self.assertTrue(isinstance(items, list))
        self.assertGreaterEqual(len(items), 1)

    def test_teams(self):
        res = self.client.get('/api/teams/')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        items = data if isinstance(data, list) else data.get('results', [])
        self.assertTrue(isinstance(items, list))

    def test_workouts(self):
        res = self.client.get('/api/workouts/')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        items = data if isinstance(data, list) else data.get('results', [])
        self.assertTrue(isinstance(items, list))

    def test_leaderboard(self):
        res = self.client.get('/api/leaderboard/')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        items = data if isinstance(data, list) else data.get('results', [])
        self.assertTrue(isinstance(items, list))
