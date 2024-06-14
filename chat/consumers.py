from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Chatroom, Message
from django.contrib.auth.models import User
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.chatroom_id = self.scope['url_route']['kwargs']['chatroom_id']
        self.room_group_name = f'chat_{self.chatroom_id}'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        if text_data:
            self.handle_message(text_data)

    def handle_message(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'message':
            message = Message(text=data['text'], chatroom=Chatroom.objects.get(id=data['chatroom_id']))
            message.user = User.objects.get(id=data['user_id'])
            message.save()
            self.send(text_data=json.dumps({
                'type': 'message',
                'text': message.text,
                'username': message.user.username,
                'chatroom_id': message.chatroom.id,
            }))

    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'message',
            'text': message['text'],
            'username': User.objects.get(id=message['user_id']).username,
            'chatroom_id': message['chatroom_id'],
        }))
