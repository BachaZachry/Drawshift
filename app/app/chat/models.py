from django.db import models
from users.models import User


class Drawing(models.Model):
    svg_file = models.FileField(upload_to="/svg_saves")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
