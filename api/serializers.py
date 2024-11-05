from django.contrib.auth.models import User
from rest_framework import serializers

from lists.models import Task, TaskList


class UserSerializer(serializers.ModelSerializer):

    tasklists = serializers.PrimaryKeyRelatedField(
        many=True, queryset=TaskList.objects.all()
    )

    class Meta:
        model = User
        fields = ("id", "username", "last_login", "date_joined", "tasklists")


class TaskListSerializer(serializers.ModelSerializer):

    creator = serializers.ReadOnlyField(source="creator.username")

    class Meta:
        model = TaskList
        fields = ("id", "title", "created_at", "creator", "tasks")


class TaskSerializer(serializers.ModelSerializer):

    creator = serializers.ReadOnlyField(source="creator.username")

    class Meta:
        model = Task
        fields = (
            "id",
            "tasklist",
            "description",
            "created_at",
            "creator",
            "is_finished",
            "finished_at",
        )
