from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from bag.context_processors import bag_contents
from home.models import Plan


class BagContextProcessorTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.plan = Plan.objects.create(
            name="Starter Plan",
            plan_type="starter",
            monthly_price=29.99,
            setup_cost=100.00,
            short_description="Simple plan",
            long_description="Long version of the plan.",
            features="One\nTwo\nThree",
        )

    def get_request_with_session(self):
        """Return a request object with a working session."""
        request = self.factory.get('/')
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()
        return request

    def test_context_processor_adds_expected_keys(self):
        request = self.get_request_with_session()
        request.session['bag'] = {str(self.plan.id): 2}  # quantity = 2

        context = bag_contents(request)

        self.assertIn('bag_items', context)
        self.assertIn('total', context)
        self.assertIn('plan_count', context)

    def test_correct_totals_and_plan_count(self):
        request = self.get_request_with_session()
        request.session['bag'] = {str(self.plan.id): 3}  # quantity = 3

        context = bag_contents(request)

        expected_total = 3 * self.plan.setup_cost
        self.assertEqual(context['total'], expected_total)
        self.assertEqual(context['plan_count'], 3)

    def test_handles_missing_plan_gracefully(self):
        request = self.get_request_with_session()
        request.session['bag'] = {'9999': 1}  # nonexistent plan ID

        context = bag_contents(request)

        self.assertEqual(context['total'], 0)
        self.assertEqual(context['plan_count'], 0)
        self.assertEqual(context['bag_items'], [])
