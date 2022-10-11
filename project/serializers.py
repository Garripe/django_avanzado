from rest_framework import serializers

from core.models import Tag, Project, Workspace


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for project objects"""

    class Meta:
        model = Project
        fields = ('id', 'name')
        read_only_fields = ('id',)


class WorkspaceSerializer(serializers.ModelSerializer):
    """Serializer for workspace objects"""
    projects = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Project.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Workspace
        fields = ('id', 'name', 'projects', 'tags')
        read_only_fields = ('id',)


class WorkspaceDetailSerializer(WorkspaceSerializer):
    """Serialize a workspace detail"""
    projects = ProjectSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
