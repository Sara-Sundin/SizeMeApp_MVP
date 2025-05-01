from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import SESSION_KEY


class AccountViewsTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@example.com",
            username="test@example.com",
            password="securepass123",
            full_name="Test User"
        )

    def test_signup_view_creates_user_and_redirects(self):
        response = self.client.post(reverse("signup"), {
            "email": "new@example.com",
            "username": "new@example.com",  # required by model
            "full_name": "New User",
            "password1": "newstrongpass123",
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("dashboard"))
        self.assertTrue(get_user_model().objects.filter(email="new@example.com").exists())
        self.assertIn(SESSION_KEY, self.client.session)

    def test_login_view_success(self):
        response = self.client.post(reverse("login"), {
            "username": "test@example.com",
            "password": "securepass123",
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("dashboard"))
        self.assertIn(SESSION_KEY, self.client.session)

    def test_dashboard_view_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")

    def test_dashboard_view_context_flags(self):
        self.client.login(email="test@example.com", password="securepass123")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/dashboard.html")
        self.assertIn("show_modal", response.context)

    def test_update_measurements_sets_session_flag(self):
        self.client.login(email="test@example.com", password="securepass123")

        # Don't follow redirect so we can inspect the session *before* dashboard_view pops it
        response = self.client.post(reverse("update_measurements"), {
            "chest": 88,
            "waist": 66,
            "hips": 90,
            "shoulders": 40,
        }, follow=False)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("dashboard"))

        # Now the session still contains the flag
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
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct")
        self.assertNotIn(SESSION_KEY, self.client.session)
