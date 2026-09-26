from django.test import TestCase

# Create your tests here.
from django.test import TestCase

from accounts.models import User
from subscriptions.models import Plan, Subscription
from .models import Payment


class PaymentModelTest(TestCase):

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

        self.subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            status=Subscription.Status.PENDING,
        )

    def test_create_payment(self):
        payment = Payment.objects.create(
            user=self.user,
            subscription=self.subscription,
            amount=100000,
        )

        self.assertEqual(payment.user, self.user)
        self.assertEqual(payment.subscription, self.subscription)
        self.assertEqual(payment.amount, 100000)
        self.assertEqual(payment.status, Payment.Status.PENDING)
        self.assertTrue(payment.authority)

    def test_payment_str(self):
        payment = Payment.objects.create(
            user=self.user,
            subscription=self.subscription,
            amount=100000,
        )

        expected = f"{self.user} - 100000 (pending)"

        self.assertEqual(str(payment), expected)

    def test_payment_success_status(self):
        payment = Payment.objects.create(
            user=self.user,
            subscription=self.subscription,
            amount=100000,
            status=Payment.Status.SUCCESS,
            ref_id="REF123456",
        )

        self.assertEqual(payment.status, Payment.Status.SUCCESS)
        self.assertEqual(payment.ref_id, "REF123456")