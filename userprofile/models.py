from django.db import models
from rest_framework.authtoken.admin import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics', null=True, blank=True)

    @classmethod
    def create(cls, user):
        user_profile = cls(user=user)
        user_profile.save()
        return user_profile
