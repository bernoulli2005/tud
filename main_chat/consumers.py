import json
from channels.generic.websocket import AsyncWebsocketConsumer
import jwt
from django.contrib.auth.models import User
from django.conf import settings
from .models import Chat, Message   

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.token = self.scope['url_route']['kwargs']['token']
        try:
            payload = jwt.decode(self.token, settings.SECRET_KEY, algorithms=['HS256'])
            self.user = User.objects.get(id=payload['user_id'])
            await self.accept()
        except:
            await self.close()

    async def disconnect(self, close_code):
        pass 

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        chat_id = text_data_json['chat_id']

        # Guardar el mensaje en la base de datos
        chat = Chat.objects.get(id=chat_id)
        message = Message.objects.create(chat=chat, sender=self.user, content=message)
        message.save()

        # Enviar el mensaje a todos los participantes del chat
        await self.send(text_data=json.dumps({
            'message': message.content,
            'sender': message.sender.username,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }))
