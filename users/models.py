from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save
import uuid


# AbstractUser._meta.get_field("email")._unique = True


class Team(models.Model):
    name = models.CharField(
        max_length=256, unique=True, null=False, default=uuid.uuid4().hex
    )


class User(AbstractUser):
    team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL)
    is_leader = models.BooleanField(default=False)
    can_invite = models.BooleanField(default=False)


class Invite(models.Model):
    STATUS_CHOICE = (("P", "Pending"), ("A", "Accepted"), ("R", "Rejected"))
    sender = models.ForeignKey(User, related_name="Sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        User, related_name="Receiver", on_delete=models.CASCADE
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICE, default="P")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.sender == self.receiver:
            raise ValidationError("Sender can't invite himself")
        elif self.receiver.team is not None:
            raise ValidationError("Receiver is already part of another team")
        else:
            super(Invite, self).save(*args, **kwargs)


@receiver(post_save, sender=Invite)
def delete_object(sender, instance, created, **kwargs):
    # If instance is being created,then we do nothing
    if created:
        pass
    # Upon modification,if the invite is accepted or rejected
    # The instance will be deleted
    elif (instance.status == "A") or (instance.status == "R"):
        instance.delete()
