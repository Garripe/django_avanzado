from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Project

from project.serializers import ProjectSerializer

PROJECTS_URL = reverse('project:project-list')


class PublicProjectsApiTests(TestCase):
    """Test the publicly available projects API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving projects"""
        res = self.client.get(PROJECTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test the authorized user tags API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_projects(self):
        """Test retrieving projects"""
        Project.objects.create(user=self.user, name='Project1')
        Project.objects.create(user=self.user, name='Project2')

        res = self.client.get(PROJECTS_URL)

        projects = Projects.objects.all().order_by('-name')
        serializer = ProjectSerializer(projects, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_projects_limited_to_user(self):
        """Test that projects returned are for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            'test2@test.com',
            'testpass'
        )
        PROJECT.objects.create(user=user2, name='Project3')
        project = PROJECT.objects.create(user=self.user, name='Project4')

        res = self.client.get(PROJECTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], project.name)
