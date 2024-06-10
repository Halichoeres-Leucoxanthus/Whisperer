from channels.generic.websocket import WebsocketConsumer
from .models import Chatroom, Message
import json
from django.contrib.auth.models import User


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None, **kwargs):
        if text_data:
            self.handle_message(text_data)

    def handle_message(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'join':
            self.send(text_data=json.dumps({
                'type': 'join',
                'chatroom_id': data['chatroom_id'],
            }))
        elif data['type'] == 'message':
            message = Message(text=data['text'], chatroom=Chatroom.objects.get(id=data['chatroom_id']))
            message.user = User.objects.get(id=data['user_id'])
            message.save()
            self.send(text_data=json.dumps({
                'type': 'message',
                'text': message.text,
                'username': message.user.username,
                'chatroom_id': message.chatroom.id,
            }))
