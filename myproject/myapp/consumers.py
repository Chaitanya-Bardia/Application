# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MailProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self): #used to connect with the WebSocket
        self.room_group_name = "mail_progress"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code): #Once connection is disconnected
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    #It receives progress updates from Celery about email sending status
    #Its job is to forward these updates to the connected WebSocket client
    async def send_email_update(self, event):
        await self.send(text_data=json.dumps({
            'emails_sent': event['emails_sent'],
            'total_emails': event['total_emails'],
        }))