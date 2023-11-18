# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Log

class LogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('logs_group', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('logs_group', self.channel_name)

    async def receive(self, text_data):
        # You can handle received data if needed
        pass

    async def log_message(self, event):
        # When a new log is ingested, this method sends the message to the WebSocket group
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}))
