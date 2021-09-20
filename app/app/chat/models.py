from django.db import models
from users.models import User
from django.contrib.postgres.fields import ArrayField


class Drawing(models.Model):
    path = ArrayField(models.JSONField(), default=[])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False, default="")


class Diagram(models.Model):
    elements = ArrayField(models.JSONField())
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False)
