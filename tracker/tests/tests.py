from django.test import TestCase
# dashboard/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from tracker.models import TrackedCoin

class DashboardTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.login_url = reverse('login')
        self.dashboard_url = reverse('dashboard')
        self.add_coin_url = self.dashboard_url  # assuming coin form is on dashboard
        self.delete_coin_url = reverse('delete_coin_ajax')

# Create your tests here.
    def test_login_view(self):
        response = self.client.post(self.login_url,
                                    {
                                        'username' :'testuser',
                                        'password' : 'testpass123'
                                    })
        self.assertEqual(response.status_code, 302)

    def test_add_coin(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.add_coin_url, {'coin_name': 'bitcoin'})
        self.assertEqual(TrackedCoin.objects.filter(user=self.user, coin_name='bitcoin').count(), 1)

    def test_prevent_duplicate_coins(self):
        self.client.login(username='testuser', password='testpass123')
        self.client.post(self.add_coin_url, {'coin_name': 'bitcoin'})
        self.client.post(self.add_coin_url, {'coin_name': 'bitcoin'})
        coins = TrackedCoin.objects.filter(user=self.user, coin_name='bitcoin')
        self.assertEqual(coins.count(), 1)  # should not allow duplicate

    def test_delete_coin_ajax(self):
        self.client.login(username='testuser', password='testpass123')
        coin = TrackedCoin.objects.create(user=self.user, coin_name='bitcoin')
        response = self.client.post(self.delete_coin_url, {'coin_id': coin.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(TrackedCoin.objects.filter(id=coin.id).exists())

    def test_dashboard_requires_login(self):
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 302)  # redirect to login
