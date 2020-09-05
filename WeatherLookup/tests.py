import unittest

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.test.client import Client

from .models import City
from .forms import CreateUserForm


class UserCreateTest(TestCase):
    def setUp(self):
        User.objects.create(username='testuser', email='kp@mail.com')

    def test_user_created(self):
        user = User.objects.get(email='kp@mail.com')
        self.assertEqual(user.email, 'kp@mail.com')


class UserLogInTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test',
                                                         password='test1919',
                                                         email='test@example.com')

    def test_correct(self):
        response = self.client.post('weather/login/', {'username': 'test', 'password': 'test1919', })
        self.assertTrue(response.status_code, 302)

    def test_wrong_username(self):
        response = self.client.post('weather/login/', {'username': 'asdasd', 'password': 'test1919', })
        self.assertTrue(response.status_code, 404)

    def test_wrong_password(self):
        response = self.client.post('weather/login/', {'username': 'test', 'password': 'test1212', })
        self.assertTrue(response.status_code, 404)


class GetViewsTest(TestCase):
    def test_index(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_sign_in(self):
        response = self.client.get('weather/login/')
        self.assertEqual(response.status_code, 404)

    def test_sign_up(self):
        response = self.client.get('weather/register/')
        self.assertEqual(response.status_code, 200)

    def test_log_out(self):
        response = self.client.get('weather/logout/')
        self.assertEqual(response.status_code, 404)

    def test_profile_hub(self):
        response = self.client.get('weather/profile/hub')
        self.assertEqual(response.status_code, 404)

    def test_profile_detail(self):
        response = self.client.get('weather/profile/detail')
        self.assertEqual(response.status_code, 404)

    def test_profile_disable(self):
        response = self.client.get('weather/profile/disable')
        self.assertEqual(response.status_code, 404)

    def test_profile_password_change(self):
        response = self.client.get('weather/profile/1/passwordchange')
        self.assertEqual(response.status_code, 404)

    def test_profile_change(self):
        response = self.client.get('weather/profile/1/infochange')
        self.assertEqual(response.status_code, 404)

    def test_about(self):
        response = self.client.get('/weather/about/')
        self.assertEqual(response.status_code, 200)

    def test_add_fav(self):
        response = self.client.get('weather/add-fav/756135')
        self.assertEqual(response.status_code, 404)

    def test_del_fav(self):
        response = self.client.get('weather/del-fav/756135')
        self.assertEqual(response.status_code, 404)

    def test_weather_detail(self):
        response = self.client.get('weather/detail/756135')
        self.assertEqual(response.status_code, 200)

    def test_weather_forecast(self):
        response = self.client.get('weather/forecast/756135')
        self.assertEqual(response.status_code, 200)
