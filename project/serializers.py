from rest_framework import serializers

from core.models import Tag, Project


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
