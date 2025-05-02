from django.test import TestCase
from home.forms import ContactForm


class ContactFormTest(TestCase):

    def test_form_valid_data(self):
        form = ContactForm(data={
            'name': 'Sara',
            'email': 'sara@example.com',
            'message': 'Hello from the test!',
        })
        self.assertTrue(form.is_valid())

    def test_form_missing_fields(self):
        form = ContactForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('message', form.errors)

    def test_email_field_custom_validation(self):
        invalid_emails = ['noatsign.com', 'missingdot@com', '']
        for bad_email in invalid_emails:
            form = ContactForm(data={
                'name': 'Sara',
                'email': bad_email,
                'message': 'Testing invalid email',
            })
            self.assertFalse(form.is_valid())
            self.assertIn('email', form.errors)

    def test_label_suffix_removed(self):
        form = ContactForm()
        for field in form.fields.values():
            self.assertEqual(field.label_suffix, '')
