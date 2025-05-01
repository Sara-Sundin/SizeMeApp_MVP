from django.test import TestCase
from accounts.forms import CustomSignupForm, CustomLoginForm, CustomUserUpdateForm
from django.contrib.auth import get_user_model


class CustomSignupFormTest(TestCase):

    def test_valid_signup_form(self):
        form_data = {
            'full_name': 'Sara Skog',
            'email': 'sara@example.com',
            'password1': 'strongpassword123',
        }
        form = CustomSignupForm(data=form_data)
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertEqual(user.full_name, 'Sara Skog')
        self.assertEqual(user.email, 'sara@example.com')
        self.assertEqual(user.username, 'sara@example.com')  # from save override

    def test_missing_full_name(self):
        form_data = {
            'email': 'no_name@example.com',
            'password1': 'strongpassword123',
        }
        form = CustomSignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('full_name', form.errors)

    def test_missing_email(self):
        form_data = {
            'full_name': 'Nameless Email',
            'password1': 'strongpassword123',
        }
        form = CustomSignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class CustomLoginFormTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='login@example.com',
            username='login@example.com',
            password='pass12345',
        )

    def test_valid_login(self):
        form_data = {
            'username': 'login@example.com',
            'password': 'pass12345',
        }
        form = CustomLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_login(self):
        form_data = {
            'username': 'login@example.com',
            'password': 'wrongpassword',
        }
        form = CustomLoginForm(data=form_data)
        self.assertFalse(form.is_valid())


class CustomUserUpdateFormTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='update@example.com',
            username='update@example.com',
            full_name='Old Name',
            password='securepass',
        )

    def test_user_update_form(self):
        form_data = {
            'full_name': 'New Name',
            'email': 'update@example.com',
        }
        form = CustomUserUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.assertEqual(updated_user.full_name, 'New Name')
