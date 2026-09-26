from django.test import TestCase

# Create your tests here.
from datetime import timedelta

from django.utils import timezone

from accounts.models import User
from .models import Plan, Subscription


class SubscriptionModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPass123",
        )

        self.plan = Plan.objects.create(
            name="Monthly Plan",
            price=100000,
            duration_days=30,
            level=1,
        )

    def test_create_plan(self):
        self.assertEqual(self.plan.name, "Monthly Plan")
        self.assertEqual(self.plan.price, 100000)
        self.assertEqual(self.plan.duration_days, 30)
        self.assertTrue(self.plan.is_active)

    def test_activate_subscription(self):
        subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
        )

        subscription.activate()
        subscription.refresh_from_db()

        self.assertEqual(subscription.status, Subscription.Status.ACTIVE)
        self.assertIsNotNone(subscription.start_at)
        self.assertIsNotNone(subscription.end_at)

        expected_end = subscription.start_at + timedelta(
            days=self.plan.duration_days
        )

        self.assertEqual(
            subscription.end_at,
            expected_end,
        )

    def test_active_queryset(self):
        subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
        )

        subscription.activate()

        active_subscriptions = Subscription.objects.active()

        self.assertIn(subscription, active_subscriptions)

    def test_subscription_str(self):
        subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
        )

        expected = f"{self.user} - {self.plan.name} (pending)"

        self.assertEqual(str(subscription), expected)