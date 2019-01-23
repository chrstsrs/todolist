from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Task(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=4000)
    issued_by = models.ForeignKey(User, related_name='issued', on_delete=models.CASCADE)
    done = models.BooleanField(default=False)
    done_by = models.ForeignKey(User, related_name='+', null=True,
                                blank=True, on_delete=models.SET_NULL)


class Preferences(models.Model):
    user = models.OneToOneField(User, related_name='+', on_delete=models.CASCADE)
    show_all = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_user_preferences(sender, instance, created, **kwargs):
    if created:
        Preferences.objects.create(user=instance)
