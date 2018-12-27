from django.db import models
from django.contrib.auth.models import User


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
