from django.test import TestCase
from django.contrib.auth import get_user_model

class UserModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'username': 'testuser'
        }
        self.superuser_data = {
            'email': 'admin@example.com',
            'password': 'adminpassword',
            'username': 'adminuser',
            'is_staff': True,
            'is_active': True,
            'is_superuser': True
        }

    def test_create_user(self):
        user = get_user_model().objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        superuser = get_user_model().objects.create_superuser(**self.superuser_data)
        self.assertEqual(superuser.email, self.superuser_data['email'])
        self.assertTrue(superuser.check_password(self.superuser_data['password']))
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_active)

    def test_permission_observer(self):
        observer_data = {
            'email': 'observer@exple.com',
            'password': 'observerpassword',
            'username': 'observeruser',
            'is_observer': True
        }
        observer = get_user_model().objects.create_user(**observer_data)
        self.assertEqual(observer.email, observer_data['email'])
        self.assertTrue(observer.check_password(observer_data['password']))
        self.assertTrue(observer.is_observer)
