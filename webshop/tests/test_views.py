from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class WebshopViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser@example.com',
            password='password123'
        )

    def test_webshop_view_sets_size_mode(self):
        response = self.client.get(reverse('webshop'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'webshop/webshop.html')
        self.assertIn('size_mode', self.client.session)
        self.assertTrue(self.client.session['size_mode'])

    def test_update_measurements_requires_login(self):
        response = self.client.post(reverse('update_measurements_from_webshop'), {
            'chest': '90',
            'waist': '70',
            'hips': '95',
            'shoulders': '45'
        })
        self.assertRedirects(
            response,
            '/accounts/login/?next=/products/update-measurements/'
        )

    def test_update_measurements_successfully_updates_user(self):
        logged_in = self.client.login(username='testuser@example.com', password='password123')
        self.assertTrue(logged_in)

        response = self.client.post(reverse('update_measurements_from_webshop'), {
            'chest': '90',
            'waist': '70',
            'hips': '95',
            'shoulders': '45'
        }, HTTP_REFERER='/webshop/')

        self.assertRedirects(response, '/webshop/')
        updated_user = User.objects.get(pk=self.user.pk)

        # Compare numerically for flexibility
        self.assertEqual(float(updated_user.chest), 90.0)
        self.assertEqual(float(updated_user.waist), 70.0)
        self.assertEqual(float(updated_user.hips), 95.0)
        self.assertEqual(float(updated_user.shoulders), 45.0)

        self.assertTrue(self.client.session.get('show_webshop_measurements_success'))
