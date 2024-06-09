from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from .models import UserProfile
from Whisperer import settings
import os


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = super().create(validated_data)
        UserProfile.objects.create(user=user)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'bio', 'profile_picture']

    def update(self, instance, validated_data):
        user = instance.user
        user.username = validated_data.get('user', {}).get('username', user.username)
        user.email = validated_data.get('user', {}).get('email', user.email)
        user.save()

        instance.bio = validated_data.get('bio', instance.bio)
        profile_picture = validated_data.get('profile_picture', instance.profile_picture)

        if profile_picture and instance.profile_picture and instance.profile_picture != profile_picture:
            old_profile_picture_path = os.path.join(settings.MEDIA_ROOT, 'profile_pics', instance.profile_picture.name)
            if os.path.exists(old_profile_picture_path):
                os.remove(old_profile_picture_path)
            instance.profile_picture = profile_picture

        instance.save()
        return instance


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError("User account is disabled.")
            else:
                # Check if the user exists but the password is incorrect
                try:
                    user = User.objects.get(username=username)
                    raise serializers.ValidationError("Invalid password.")
                except User.DoesNotExist:
                    raise serializers.ValidationError("Invalid username.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        return data
