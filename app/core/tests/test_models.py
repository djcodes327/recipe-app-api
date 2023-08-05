"""
Test for Models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
    """Test User Models."""

    def test_create_user_with_email_successful(self):
        """Test Creating a user with an email is successfull."""
        email = "djoshi@example.com"
        password = "Test@1234"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test New User Email is Normalized or not."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.com', 'test4@example.com'],
        ]

        for email, normalized_email in sample_emails:
            user = get_user_model().objects.create_user(
                email=email,
                password='Sample@123',
            )
            self.assertEqual(user.email, normalized_email)

    def test_new_user_without_email_raises_error(self):
        """Test New user without email raises an ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test@123')

    def test_create_superuser(self):
        """Test Super User creation."""
        user = get_user_model().objects.create_superuser(
            email="test@example.com",
            password="Sample@123",
        )

        self.assertEqual(user.is_superuser, True)
        self.assertEqual(user.is_staff, True)
