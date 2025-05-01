from django.test import TestCase
from django.contrib.auth import get_user_model


class CustomUserModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            username='testuser',
            password='securepass123',
            full_name='Sara Skog',
            chest=90.5,
            waist=70.0,
            hips=95.2,
            shoulders=45.0,
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.full_name, 'Sara Skog')
        self.assertEqual(self.user.chest, 90.5)

    def test_get_full_name(self):
        self.assertEqual(self.user.get_full_name(), 'Sara Skog')

    def test_get_short_name(self):
        self.assertEqual(self.user.get_short_name(), 'Sara')

    def test_string_representation(self):
        self.assertEqual(str(self.user), 'Sara')
