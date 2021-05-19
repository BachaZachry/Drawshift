from django.db import models
from django.urls import reverse

# Create your models here.
class task(models.Model):
    title=models.TextField()
    description=models.TextField()
    member=models.TextField()
    groupe=models.TextField(default='Group1TheBest')
    a = models.BooleanField(default='True')
    
    def get_absolute_url(self):
         return reverse("tasks:taskDetail",kwargs={"id":self.id})
    