from django.db import models
from users.models import User
from django.contrib.postgres.fields import ArrayField

# from storages.backends.s3boto3 import S3Boto3Storage
# from app.settings import AWS_STORAGE_BUCKET_NAME


class Drawing(models.Model):
    path = ArrayField(models.JSONField(), default=list())
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False, default="")
    # image = models.FileField(
    #     storage=S3Boto3Storage(bucket_name=AWS_STORAGE_BUCKET_NAME)
    # )
    base64_image = models.TextField(null=True, blank=True)


class Diagram(models.Model):
    elements = ArrayField(models.JSONField())
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False)
