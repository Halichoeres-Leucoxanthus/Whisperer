from django.db import models
from django.contrib.auth.models import User


class Chatroom(models.Model):
    users = models.ManyToManyField(User)
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name = 'Chatroom'
        verbose_name_plural = 'Chatrooms'

    def __str__(self):
        return self.name
