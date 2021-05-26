from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save

class User(AbstractUser):
    pass


class Invite(models.Model):
    STATUS_CHOICE = (
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('R', 'Rejected')
    )
    sender = models.ForeignKey(User,related_name="Sender",on_delete=models.CASCADE)
    receiver = models.ForeignKey(User,related_name="Receiver",on_delete=models.CASCADE)
    status = models.CharField(max_length=1,choices=STATUS_CHOICE,default='P')

    def save(self,*args,**kwargs):
        if (self.sender==self.receiver):
            raise ValidationError("Sender can't invite himself")
        else:
            super(Invite,self).save(*args,**kwargs)


@receiver(post_save, sender=Invite)
def delete_object(sender, instance, created, **kwargs):
    # If instance is being created,then we do nothing
    if created:
        pass
    # Upon modification,if the invite is accepted or rejected
    # The instance will be deleted
    elif (instance.status == 'A') or (instance.status == 'R'):
        instance.delete()
