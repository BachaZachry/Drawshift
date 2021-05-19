from django.db import models

# Create your models here.

# Create your models here.
class article(models.Model):
    title=models.TextField()
    text=models.TextField()
    writer=models.TextField(default='writer')
   