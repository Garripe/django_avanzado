from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@tes.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@test.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@TEST.COM'
        user = get_user_model().objects.create_user(
            email,
            password='Testpass123'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'Testpass123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        email = 'test@test.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_superuser(
            email,
            password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Project1'
        )
        self.assertEqual(str(tag), tag.name)

    def test_projects_str(self):
        """Test the project string representation"""
        project = models.Project.objects.create(
            user=sample_user(),
            name='project001'
        )
        self.assertEqual(str(project), project.name)

    def test_workspace_str(self):
        """Test the workspace string representation"""
        workspace = models.Workspace.objects.create(
            user=sample_user(),
            name='workspace001'
        )
        self.assertEqual(str(workspace), workspace.name)
