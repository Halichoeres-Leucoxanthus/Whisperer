from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone

class Chatroom(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=10, choices=['private', 'global'])
    users = models.ManyToManyField(User, related_name='chatrooms', blank=True)



    def str(self):
        return self.name

class Message(models.Model):
    chatroom = models.ForeignKey(Chatroom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"Message in {self.chatroom.name} by {self.user.username}"