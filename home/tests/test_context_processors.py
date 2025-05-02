from django.test import RequestFactory, TestCase
from home.context_processors import global_context
from home.forms import ContactForm

class GlobalContextProcessorTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_global_context_includes_contact_form_and_modal_flag(self):
        request = self.factory.get('/')
        request.session = {'show_success_modal': True}
        context = global_context(request)

        self.assertIn('contact_form', context)
        self.assertIsInstance(context['contact_form'], ContactForm)

        self.assertIn('show_success_modal', context)
        self.assertTrue(context['show_success_modal'])

        # Check that flag is popped from session
        self.assertNotIn('show_success_modal', request.session)

    def test_global_context_without_modal_flag(self):
        request = self.factory.get('/')
        request.session = {}  # No 'show_success_modal' set
        context = global_context(request)

        self.assertIn('contact_form', context)
        self.assertIsInstance(context['contact_form'], ContactForm)

        self.assertIn('show_success_modal', context)
        self.assertFalse(context['show_success_modal'])  # Should default to False

