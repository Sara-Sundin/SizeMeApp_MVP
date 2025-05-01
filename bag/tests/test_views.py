from django.test import TestCase
from django.urls import reverse
from home.models import Plan


class BagViewsTest(TestCase):

    def setUp(self):
        self.plan = Plan.objects.create(
            name="Test Plan",
            plan_type="starter",  # must match one of your choices
            monthly_price=29.99,
            setup_cost=100.00,
            short_description="A great starter option",
            long_description="This is a long description for testing purposes.",
            features="Feature 1\nFeature 2\nFeature 3",
        )

    def test_view_bag_empty(self):
        response = self.client.get(reverse("view_bag"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bag/bag.html")
        self.assertContains(response, "bag")  # Basic presence check

    def test_add_to_bag(self):
        response = self.client.post(reverse("add_to_bag", args=[self.plan.id]), {
            "quantity": 2,
            "redirect_url": reverse("view_bag")
        })
        self.assertRedirects(response, reverse("view_bag") + "?added=true")

        session_bag = self.client.session.get("bag", {})
        self.assertIn(str(self.plan.id), session_bag)
        self.assertEqual(session_bag[str(self.plan.id)], 2)

    def test_add_to_bag_invalid_quantity(self):
        response = self.client.post(reverse("add_to_bag", args=[self.plan.id]), {
            "quantity": "invalid",
            "redirect_url": reverse("view_bag")
        })
        self.assertRedirects(response, reverse("home"))  # fallback redirect


    def test_adjust_bag_quantity(self):
        # First add an item
        self.client.post(reverse("add_to_bag", args=[self.plan.id]), {
            "quantity": 1,
            "redirect_url": reverse("view_bag")
        })
        # Now adjust quantity
        response = self.client.post(reverse("adjust_bag", args=[self.plan.id]), {
            "quantity": 3
        })
        self.assertRedirects(response, reverse("view_bag"))

        session_bag = self.client.session.get("bag", {})
        self.assertEqual(session_bag[str(self.plan.id)], 3)

    def test_adjust_bag_to_zero_removes_item(self):
        # Add item
        self.client.post(reverse("add_to_bag", args=[self.plan.id]), {
            "quantity": 1,
            "redirect_url": reverse("view_bag")
        })
        # Remove it
        response = self.client.post(reverse("adjust_bag", args=[self.plan.id]), {
            "quantity": 0
        })
        self.assertRedirects(response, reverse("view_bag"))

        session_bag = self.client.session.get("bag", {})
        self.assertNotIn(str(self.plan.id), session_bag)

    def test_remove_from_bag(self):
        self.client.post(reverse("add_to_bag", args=[self.plan.id]), {
            "quantity": 1,
            "redirect_url": reverse("view_bag")
        })
        response = self.client.post(reverse("remove_from_bag", args=[self.plan.id]))
        self.assertEqual(response.status_code, 200)

        session_bag = self.client.session.get("bag", {})
        self.assertNotIn(str(self.plan.id), session_bag)
