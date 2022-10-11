from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Workspace, Project, Tag

from project.serializers import WorkspaceSerializer, ProjectSerializer, TagSerializer, WorkspaceDetailSerializer

WORKSPACE_URL = reverse('project:workspace-list')


def sample_workspace(user, **params):
    """Create and return a sample workspace"""
    defaults = {
        'name': 'Sample workspace',
    }
    defaults.update(params)

    return Workspace.objects.create(user=user, **defaults)


def sample_project(user, name='Sample project'):
    """Create and return a sample project"""

    return Project.objects.create(user=user, name=name)


def detail_url(workspace_id):
    """Return workspace detail URL"""
    return reverse('project:workspace-detail', args=[workspace_id])


def sample_tag(user, name='Sample tag'):
    """Create and return a sample tag"""
    return Tag.objects.create(user=user, name=name)


class PublicWorkspaceApiTests(TestCase):
    """Test the publicly available workspace API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving workspaces"""
        res = self.client.get(WORKSPACE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateWorkspaceApiTests(TestCase):
    """Test the authorized user workspace API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test1@test.com',
            'testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_workspace(self):
        """Test retrieving workspace"""
        sample_workspace(user=self.user)
        sample_workspace(user=self.user)

        res = self.client.get(WORKSPACE_URL)

        workspaces = Workspace.objects.all().order_by('id')
        serializer = WorkspaceSerializer(workspaces, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_workspaces_limited_to_user(self):
        """Test that workspaces returned are for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            'test2@test.com',
            'testpass'
        )
        sample_workspace(user=user2)
        sample_workspace(user=self.user)

        res = self.client.get(WORKSPACE_URL)

        workspaces = Workspace.objects.filter(user=self.user)
        serializer = WorkspaceSerializer(workspaces, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_workspace_detail(self):
        """Test viewing a workspace detail"""
        workspace = sample_workspace(user=self.user)
        workspace.projects.add(sample_project(user=self.user))
        workspace.tags.add(sample_tag(user=self.user))

        url = detail_url(workspace.id)
        res = self.client.get(url)

        serializer = WorkspaceDetailSerializer(workspace)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_workspace(self):
        """Test creating workspace"""
        payload = {
            'name': 'Test workspace',
        }
        res = self.client.post(WORKSPACE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        workspace = Workspace.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(workspace, key))

    def test_create_workspace_with_tags(self):
        """Test creating a workspace with projects"""
        tag1 = sample_tag(user=self.user, name='Tag 1')
        tag2 = sample_tag(user=self.user, name='Tag 2')
        payload = {
            'name': 'Test workspace',
            'tags': [tag1.id, tag2.id]
        }
        res = self.client.post(WORKSPACE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        workspace = Workspace.objects.get(id=res.data['id'])
        tags = workspace.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_workspace_with_projects(self):
        """Test creating a workspace with projects"""
        project1 = sample_project(user=self.user, name='Project 1')
        project2 = sample_project(user=self.user, name='Project 2')
        payload = {
            'name': 'Test workspace',
            'projects': [project1.id, project2.id]
        }
        res = self.client.post(WORKSPACE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        workspace = Workspace.objects.get(id=res.data['id'])
        projects = workspace.projects.all()
        self.assertEqual(projects.count(), 2)
        self.assertIn(project1, projects)
        self.assertIn(project2, projects)
