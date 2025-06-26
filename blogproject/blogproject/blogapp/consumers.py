import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Obtener los últimos 50 mensajes
        last_messages = await self.get_last_messages()
        for msg in reversed(last_messages):
            await self.send(text_data=json.dumps({
                'message': msg.message,
                'user': msg.user.username if msg.user else 'Anónimo',
                'type': 'chat_message',
            }))

    @database_sync_to_async
    def get_last_messages(self):
        return list(ChatMessage.objects.filter(room_name=self.room_name).select_related('user').order_by('-timestamp')[:50])

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'chat_message':
            message = data['message']
            user = self.scope["user"]

            if user.is_authenticated:
                saved_message = await self.save_message(user, message)
                username = user.username
                message_id = saved_message.id
            else:
                username = 'Anónimo'
                message_id = None

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': username,
                    'id': message_id,
                }
            )
        elif message_type == 'typing_status':
            user = self.scope["user"]
            username = user.username if user.is_authenticated else 'Anónimo'
            status = data.get('status')
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_status',
                    'username': username,
                    'status': status,
                }
            )
        elif message_type == 'edit_message':
            message_id = data.get('id')
            new_text = data.get('new_message')
            user = self.scope["user"]
            if user.is_authenticated and message_id and new_text is not None:
                updated = await self.update_message(user, message_id, new_text)
                if updated:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'edit_message',
                            'id': message_id,
                            'new_message': new_text,
                        }
                    )
        elif message_type == 'delete_message':
            message_id = data.get('id')
            user = self.scope["user"]
            if user.is_authenticated and message_id:
                deleted = await self.remove_message(user, message_id)
                if deleted:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'delete_message',
                            'id': message_id,
                        }
                    )

    @database_sync_to_async
    def save_message(self, user, message):
        return ChatMessage.objects.create(user=user, message=message, room_name=self.room_name)

    @database_sync_to_async
    def update_message(self, user, message_id, new_text):
        try:
            msg = ChatMessage.objects.get(id=message_id)
            if msg.user == user:
                msg.message = new_text
                msg.save()
                return True
            return False
        except ChatMessage.DoesNotExist:
            return False

    @database_sync_to_async
    def remove_message(self, user, message_id):
        try:
            msg = ChatMessage.objects.get(id=message_id)
            if msg.user == user:
                msg.delete()
                return True
            return False
        except ChatMessage.DoesNotExist:
            return False

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'user': event['user'],
            'id': event.get('id'),
        }))

    async def typing_status(self, event):
        # Enviar el estado de escritura directamente al cliente
        await self.send(text_data=json.dumps({
            'type': 'typing_status',
            'username': event['username'],
            'status': event['status'],
        }))

    async def edit_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'edit_message',
            'id': event['id'],
            'new_message': event['new_message'],
        }))

    async def delete_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'delete_message',
            'id': event['id'],
        }))
