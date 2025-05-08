from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import SESSION_KEY

User = get_user_model()

class AccountViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            username="test@example.com",
            password="securepass123",
            full_name="Test User"
        )

    def test_signup_view_creates_user_and_redirects(self):
        response = self.client.post(reverse("signup"), {
            "email": "new@example.com",
            "username": "new@example.com",
            "full_name": "New User",
            "password1": "newstrongpass123",
        })
        self.assertRedirects(response, reverse("dashboard"))
        self.assertTrue(User.objects.filter(email="new@example.com").exists())
        self.assertIn(SESSION_KEY, self.client.session)

    def test_login_view_success(self):
        response = self.client.post(reverse("login"), {
            "username": "test@example.com",
            "password": "securepass123",
        })
        self.assertRedirects(response, reverse("dashboard"))
        self.assertIn(SESSION_KEY, self.client.session)

    def test_dashboard_view_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")

    def test_dashboard_view_context_flags(self):
        self.client.login(email="test@example.com", password="securepass123")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("show_modal", response.context)

    def test_update_measurements_sets_session_flag(self):
        self.client.login(email="test@example.com", password="securepass123")
        response = self.client.post(reverse("update_measurements"), {
            "chest": 88, "waist": 66, "hips": 90, "shoulders": 40
        }, follow=False)
        session = self.client.session
        self.assertTrue(session.get("show_measurements_updated_modal", False))

    def test_profile_update_view(self):
        self.client.login(email="test@example.com", password="securepass123")
        response = self.client.post(reverse("update_profile"), {
            "full_name": "Updated Name",
            "email": "test@example.com",
        })
        self.assertRedirects(response, reverse("dashboard"))
        self.user.refresh_from_db()
        self.assertEqual(self.user.full_name, "Updated Name")

    def test_login_with_wrong_password_fails(self):
        response = self.client.post(reverse("login"), {
            "username": "test@example.com",
            "password": "wrongpassword",
        })
        self.assertContains(response, "Please enter a correct")
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_login_update_measurements_sets_redirect_flag(self):
        self.client.login(email="test@example.com", password="securepass123")
        response = self.client.post(reverse("login_update_measurements"), {
            "chest": 88, "waist": 66, "hips": 90, "shoulders": 40
        }, follow=False)
        session = self.client.session
        self.assertTrue(session.get("show_redirect_modal", False))

    def test_delete_measurements_clears_fields_and_sets_flag(self):
        self.client.login(email="test@example.com", password="securepass123")
        self.user.chest = 90
        self.user.save()
        response = self.client.post(reverse("delete_measurements"), follow=False)
        self.user.refresh_from_db()
        self.assertIsNone(self.user.chest)
        session = self.client.session
        self.assertTrue(session.get("show_measurements_deleted_modal", False))

    def test_delete_account_removes_user_and_sets_flag(self):
        self.client.login(email="test@example.com", password="securepass123")
        response = self.client.post(reverse("delete_account"), follow=False)
        self.assertFalse(User.objects.filter(email="test@example.com").exists())
        session = self.client.session
        self.assertTrue(session.get("show_account_deleted_modal", False))

    def test_custom_logout_sets_flag_and_logs_out(self):
        self.client.login(email="test@example.com", password="securepass123")
        response = self.client.get(reverse("custom_logout"), follow=False)
        self.assertNotIn(SESSION_KEY, self.client.session)
        session = self.client.session
        self.assertTrue(session.get("show_logged_out_modal", False))

    def test_update_avatar_valid_and_invalid(self):
        self.client.login(email="test@example.com", password="securepass123")

        # Valid
        self.client.post(reverse("update_avatar"), {"avatar_number": "5"})
        self.user.refresh_from_db()
        self.assertEqual(self.user.avatar_number, 5)

        # Invalid
        response = self.client.post(reverse("update_avatar"), {"avatar_number": "20"})
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any("Invalid avatar" in str(m) for m in messages))
