from django import forms
from .models import Chatroom


class ChatroomForm(forms.ModelForm):
    class Meta:
        model = Chatroom
        fields = ('name', 'description')
