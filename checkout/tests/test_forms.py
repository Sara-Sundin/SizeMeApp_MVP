from django.test import TestCase
from checkout.forms import OrderForm


class OrderFormTest(TestCase):

    def setUp(self):
        self.valid_data = {
            'full_name': 'Sara Skog',
            'email': 'sara@example.com',
            'phone_number': '123456789',
            'street_address1': 'Main St 1',
            'street_address2': '',
            'town_or_city': 'Gothenburg',
            'postcode': '41101',
            'country': 'SE',
            'county': 'Västra Götaland',
        }

    def test_order_form_valid_data(self):
        form = OrderForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_order_form_missing_required_field(self):
        invalid_data = self.valid_data.copy()
        invalid_data['full_name'] = ''  # Required
        form = OrderForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('full_name', form.errors)

    def test_field_placeholders_and_classes(self):
        form = OrderForm()
        expected_placeholders = {
            'full_name': 'Full Name *',
            'email': 'Email Address *',
            'phone_number': 'Phone Number *',
            'street_address1': 'Street Address 1 *',
            'street_address2': 'Street Address 2',
            'town_or_city': 'Town or City *',
            'postcode': 'Postal Code *',
            'county': 'County, State or Locality',
        }

        for field_name, expected_placeholder in expected_placeholders.items():
            field = form.fields[field_name]
            self.assertEqual(
                field.widget.attrs.get('placeholder'),
                expected_placeholder,
                msg=f"{field_name} has incorrect placeholder",
            )
            self.assertEqual(
                field.widget.attrs.get('class'),
                'stripe-style-input',
                msg=f"{field_name} missing correct CSS class",
            )

        # Check autofocus only on full_name
        self.assertTrue(form.fields['full_name'].widget.attrs.get('autofocus', False))

    def test_all_labels_are_removed(self):
        form = OrderForm()
        for field in form.fields:
            self.assertFalse(
                form.fields[field].label,
                msg=f"{field} should have no label"
            )
