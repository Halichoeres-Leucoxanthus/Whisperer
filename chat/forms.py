from django import forms
from .models import Chatroom, Message


class ChatroomForm(forms.ModelForm):
    class Meta:
        model = Chatroom
        fields = ('name', 'description')


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('text',)
