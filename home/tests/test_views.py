from django.test import TestCase, Client
from django.urls import reverse
from home.models import Plan


class HomeViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.index_url = reverse('home')
        self.plan_url = reverse('plan')
        self.contact_url = reverse('contact')
        self.plan = Plan.objects.create(name='Starter', setup_cost=10.00, monthly_price=2.50)

    def test_index_view_context(self):
        session = self.client.session
        session['show_success_modal'] = True
        session['show_logged_out_modal'] = True
        session['show_account_deleted_modal'] = True
        session.save()

        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertIn('contact_form', response.context)
        self.assertTrue(response.context['show_success_modal'])
        self.assertTrue(response.context['show_logged_out_modal'])
        self.assertTrue(response.context['show_account_deleted_modal'])

    def test_plan_view_displays_plans(self):
        response = self.client.get(self.plan_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Starter')
        self.assertTemplateUsed(response, 'home/plan.html')

    def test_contact_post_valid_form(self):
        data = {
            'name': 'Sara',
            'email': 'sara@example.com',
            'message': 'Test message'
        }
        response = self.client.post(self.contact_url, data)
        self.assertEqual(response.status_code, 302)  # Redirects back

    def test_contact_post_invalid_form(self):
        data = {
            'name': '',
            'email': 'bademail',
            'message': ''
        }
        response = self.client.post(self.contact_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

    def test_contact_get_redirects(self):
        response = self.client.get(self.contact_url)
        self.assertEqual(response.status_code, 302)
