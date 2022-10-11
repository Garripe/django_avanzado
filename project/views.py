from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Project, Workspace

from project import serializers

# Create your views here


class BaseProjectAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Base viewset for user owned project attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(
            user=self.request.user
        ).order_by('-name')

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseProjectAttrViewSet):
    """Manage tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class ProjectViewSet(BaseProjectAttrViewSet):
    """Manage projects in the database"""
    queryset = Project.objects.all()
    serializer_class = serializers.ProjectSerializer


class WorkspaceViewSet(viewsets.ModelViewSet):
    """Manage workspaces in the database"""
    serializer_class = serializers.WorkspaceSerializer
    queryset = Workspace.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the workspaces for the authenticated user"""
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.WorkspaceDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new workspace"""
        serializer.save(user=self.request.user)
