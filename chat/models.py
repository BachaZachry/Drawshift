from django.db import models
from users.models import User
from django.contrib.postgres.fields import ArrayField


class Drawing(models.Model):
    path = ArrayField(models.JSONField(), default=list())
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False, default="")
    base64_image = models.TextField(null=True, blank=True)


class Diagram(models.Model):
    elements = ArrayField(models.JSONField())
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False)
