# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from time import sleep
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@shared_task
def send_bulk_email(recipients):
    total_emails = len(recipients)
    channel_layer = get_channel_layer()

    for i, email in enumerate(recipients):
        # Send the email
        send_mail(
            'Subject', 
            'Message', 
            'chaitanyabardia@gmail.com',  # Use your email account
            [email]
        )
        sleep(1)  # adjust according to need,keeping it 1 for now.

        #Sending progress update
        async_to_sync(channel_layer.group_send)(
            'mail_progress',
            {
                'type': 'send_email_update',
                'emails_sent': i + 1,
                'total_emails': total_emails
            }
        )
        print(f"Sent email {i+1} of {total_emails}")