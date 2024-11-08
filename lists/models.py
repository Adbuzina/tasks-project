from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class TaskList(models.Model):
    title = models.CharField(max_length=128, default="Задачи")
    created_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(
        User, null=True, related_name="tasklists", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return self.title

    def count(self):
        return self.tasks.count()

    def count_finished(self):
        return self.tasks.filter(is_finished=True).count()

    def count_open(self):
        return self.tasks.filter(is_finished=False).count()


class Task(models.Model):
    description = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField(null=True)
    is_finished = models.BooleanField(default=False)
    creator = models.ForeignKey(
        User, null=True, related_name="tasks", on_delete=models.CASCADE
    )
    tasklist = models.ForeignKey(
        TaskList, related_name="tasks", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return self.description

    def close(self):
        self.is_finished = True
        self.finished_at = timezone.now()
        self.save()

    def reopen(self):
        self.is_finished = False
        self.finished_at = None
        self.save()
