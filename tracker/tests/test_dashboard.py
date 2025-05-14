from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from tracker.models import TrackedCoin
from bs4 import BeautifulSoup



class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='sabahat', password='testpass')
        self.dashboard_url = reverse('dashboard')

    def test_dashboard_requires_login(self):
        # Without login, should redirect to login page
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_dashboard_loads_for_logged_in_user(self):
        self.client.login(username='sabahat', password='testpass')
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to Your Crypto Dashboard")

    def test_dashboard_shows_only_user_coins(self):
        # Add coin for self.user
        TrackedCoin.objects.create(user=self.user, coin_name='bitcoin')

        # Add coin for another user
        other_user = User.objects.create_user(username='omar', password='1234')
        TrackedCoin.objects.create(user=other_user, coin_name='ethereum')

        self.client.login(username='sabahat', password='testpass')
        response = self.client.get(self.dashboard_url)

        # Check that user's own coin appears
        self.assertContains(response, 'Bitcoin')
        soup = BeautifulSoup(response.content, 'html.parser')
        coin_list = soup.find(id="tracked-coins").get_text()

        self.assertNotIn('Ethereum', coin_list)
