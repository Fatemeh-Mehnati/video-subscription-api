from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.db import IntegrityError

from .models import User


class UserModelTest(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPass123",
            phone_number="09123456789",
        )

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.phone_number, "09123456789")
        self.assertTrue(user.check_password("TestPass123"))

    def test_email_must_be_unique(self):
        User.objects.create_user(
            username="user1",
            email="test@example.com",
            password="TestPass123",
        )

        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username="user2",
                email="test@example.com",
                password="TestPass123",
            )

    def test_user_str(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPass123",
        )

        self.assertEqual(str(user), "testuser")