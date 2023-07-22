from django.db import models
from django.contrib.auth.models import User


class ToDo(models.Model):
    title = models.CharField(max_length=200)
    important = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    goal_time = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
