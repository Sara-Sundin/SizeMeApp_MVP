from io import BytesIO
from PIL import Image
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from products.models import Product, Category

User = get_user_model()

def get_test_image():
    image = Image.new('RGB', (100, 100), color='blue')
    buffer = BytesIO()
    image.save(buffer, format='JPEG')
    return SimpleUploadedFile("test.jpg", buffer.getvalue(), content_type="image/jpeg")


@override_settings(DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage')
class ProductViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='tshirts', friendly_name='T-Shirts')
        self.product = Product.objects.create(
            name='Test Shirt',
            description='A great shirt.',
            price=19.99,
            category=self.category,
        )

        # Superuser (username = email for login compatibility)
        self.superuser = User.objects.create_user(
            username='admin@test.com', email='admin@test.com',
            password='adminpass', is_superuser=True, is_staff=True
        )

        # Regular user
        self.user = User.objects.create_user(
            username='user@test.com', email='user@test.com',
            password='userpass'
        )

    def test_all_products_view(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertIn(self.product, response.context['products'])

    def test_product_detail_view(self):
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_add_product_requires_login(self):
        response = self.client.get(reverse('add_product'))
        self.assertRedirects(response, '/accounts/login/?next=/products/add/')

    def test_add_product_as_superuser(self):
        self.assertTrue(self.client.login(username='admin@test.com', password='adminpass'))

        image = get_test_image()
        response = self.client.post(reverse('add_product'), {
            'name': 'New Product',
            'description': 'Nice.',
            'price': 10.00,
            'category': self.category.id,
            'has_sizes': False,
            'image': image,
            'sort_order': 1,
        })

        if response.status_code == 200 and 'form' in response.context:
            print("Add Product Form errors:", response.context['form'].errors)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Product.objects.filter(name='New Product').exists())

    def test_edit_product_requires_superuser(self):
        self.assertTrue(self.client.login(username='user@test.com', password='userpass'))
        response = self.client.get(reverse('edit_product', args=[self.product.id]))
        self.assertRedirects(response, reverse('webshop'))

    def test_edit_product_as_superuser(self):
        self.assertTrue(self.client.login(username='admin@test.com', password='adminpass'))

        response = self.client.post(reverse('edit_product', args=[self.product.id]), {
            'name': 'Updated Product',
            'description': 'Updated desc.',
            'price': 25.00,
            'category': self.category.id,
            'has_sizes': False,
            'sort_order': 1,
        })

        if response.status_code == 200 and 'form' in response.context:
            print("Edit Product Form errors:", response.context['form'].errors)

        self.assertRedirects(response, reverse('product_detail', args=[self.product.id]))
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')

    def test_delete_product(self):
        self.assertTrue(self.client.login(username='admin@test.com', password='adminpass'))
        response = self.client.post(reverse('delete_product', args=[self.product.id]))
        self.assertRedirects(response, reverse('products'))
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())