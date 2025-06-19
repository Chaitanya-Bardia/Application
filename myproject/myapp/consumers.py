# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger(__name__)

class MailProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "mail_progress"
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        logger.info(f"WebSocket connected: {self.channel_name}")

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        logger.info(f"WebSocket disconnected: {self.channel_name}")

    async def receive(self, text_data):

        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type', 'unknown')
            
            if message_type == 'ping':
                await self.send(text_data=json.dumps({
                    'type': 'pong',
                    'message': 'Connection is alive'
                }))
                
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON received: {text_data}")

    async def send_email_update(self, event):

        try:
            await self.send(text_data=json.dumps({
                'type': 'progress_update',
                'emails_sent': event['emails_sent'],
                'total_emails': event['total_emails'],
                'successful_emails': event.get('successful_emails', 0),
                'failed_emails': event.get('failed_emails', 0),
                'current_email': event.get('current_email', ''),
                'status': event.get('status', 'processing'),
                'percentage': round((event['emails_sent'] / event['total_emails']) * 100, 2)
            }))

        except Exception as e:
            logger.error(f"Error sending email update: {str(e)}")


    async def send_email_complete(self, event):
        try:
            await self.send(text_data=json.dumps({
                'type': 'completion',
                'emails_sent': event['emails_sent'],
                'total_emails': event['total_emails'],
                'successful_emails': event['successful_emails'],
                'failed_emails': event['failed_emails'],
                'failed_list': event.get('failed_list', []),
                'status': 'completed',
                'percentage': 100
            }))

        except Exception as e:
            logger.error(f"Error sending completion message: {str(e)}")