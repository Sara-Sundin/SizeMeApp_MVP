from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from products.models import Product, Category
from sizemeapp.models import GarmentFit

User = get_user_model()

class SizeMeAppViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='tshirts', friendly_name='T-Shirts')
        self.product = Product.objects.create(
            name='Test Shirt',
            description='Basic tee',
            price=20.00,
            category=self.category,
        )
        GarmentFit.objects.create(product=self.product, size_label="M", chest=100.0)

        self.user = User.objects.create_user(
            username='user@test.com', email='user@test.com', password='pass123', chest=98
        )

    def test_size_recommendation_unauthenticated(self):
        url = reverse('size_recommendation', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['recommendations'], [])

    def test_size_recommendation_authenticated_with_chest(self):
        self.client.login(username='user@test.com', password='pass123')
        url = reverse('size_recommendation', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json()['recommendations'], list)

    def test_size_recommendation_invalid_product(self):
        self.client.login(username='user@test.com', password='pass123')
        url = reverse('size_recommendation', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_toggle_size_mode_on_and_off(self):
        session = self.client.session
        session['size_mode'] = False
        session.save()

        response = self.client.get(reverse('toggle_size_mode'), follow=True)
        self.assertRedirects(response, '/webshop/')
        self.assertTrue(self.client.session['size_mode'])
        self.assertTrue(self.client.session['size_mode_entered'])

        response = self.client.get(reverse('toggle_size_mode'), follow=True)
        self.assertFalse(self.client.session['size_mode'])
        self.assertTrue(self.client.session['size_mode_exited'])
