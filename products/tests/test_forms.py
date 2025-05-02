from django.test import TestCase
from products.forms import ProductForm
from products.models import Category, Product
from products.widgets import CustomClearableFileInput

class ProductFormTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='jackets', friendly_name='Jackets')

    def test_form_fields_have_correct_css_class(self):
        form = ProductForm()
        for name, field in form.fields.items():
            self.assertIn('class', field.widget.attrs)
            self.assertEqual(field.widget.attrs['class'], 'border-black rounded-0')

    def test_category_choices_use_friendly_names(self):
        form = ProductForm()
        category_choices = form.fields['category'].choices
        self.assertIn((self.category.id, self.category.get_friendly_name()), category_choices)

    def test_image_field_uses_custom_widget(self):
        form = ProductForm()
        self.assertIsInstance(form.fields['image'].widget, CustomClearableFileInput)

    def test_valid_form_data(self):
        form_data = {
            'category': self.category.id,
            'name': 'Test Product',
            'description': 'A sample product.',
            'price': 49.99,
            'has_sizes': False,
        }
        form = ProductForm(data=form_data)
        self.assertTrue(form.is_valid())
