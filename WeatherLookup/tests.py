import unittest

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.test.client import Client
from django.urls import reverse

from .models import City, Favorite
from .forms import CreateUserForm


class UserCreateTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='kp@mail.com')

    def test_user_created(self):
        user = User.objects.get(email='kp@mail.com')
        self.assertEqual(user.email, 'kp@mail.com')

    def tearDown(self):
        self.user.delete()


class GetViewsTest(TestCase):
    def test_index(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_sign_in(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_sign_up(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_log_out(self):
        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_profile_hub(self):
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_profile_detail(self):
        url = reverse('profile_detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_profile_disable(self):
        url = reverse('disable_acc')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_profile_password_change(self):
        url = reverse('profile_pass_change', kwargs={'user_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_profile_change(self):
        url = reverse('profile_info_change', kwargs={'user_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_about(self):
        url = reverse('about')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_fav(self):
        url = reverse('add_fav', kwargs={'city_id': 756135})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_del_fav(self):
        url = reverse('del_fav', kwargs={'city_id': 756135})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_weather_detail(self):
        url = reverse('weather_detail', kwargs={'city_id': 756135})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_weather_forecast(self):
        url = reverse('weather_forecast', kwargs={'city_id': 756135})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


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


class LoggedInUserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='kp@mail.com', password='asdasd')
        self.client.login(username=self.user.username, password='asdasd')
        City.objects.all().delete()

    def tearDown(self):
        self.user.delete()

    def test_add_fav(self):
        url = reverse('add_fav', kwargs={'city_id': 756135})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(City.objects.all().count(), 1)
        city = City.objects.get(name='Warsaw')
        fav = Favorite.objects.get(city=city)
        user = User.objects.get(username='testuser')
        self.assertTrue(fav.user == user)

    def test_del_fav(self):
        add_url = reverse('add_fav', kwargs={'city_id': 756135})
        self.client.post(add_url)
        del_url = reverse('del_fav', kwargs={'city_id': 756135})
        response = self.client.post(del_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Favorite.objects.all().count(), 0)
