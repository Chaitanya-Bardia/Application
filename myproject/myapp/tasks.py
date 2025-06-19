# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.core.mail import BadHeaderError
from time import sleep
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging

# Set up logging
logger = logging.getLogger(__name__)

@shared_task(bind=True)
def send_bulk_email(self, recipients):
    total_emails = len(recipients)
    channel_layer = get_channel_layer()
    successful_emails = 0
    failed_emails = []

    logger.info(f"Starting bulk email task for {total_emails} recipients")

    for i, email in enumerate(recipients):
        try:
            # Send the email
            send_mail(
                subject='Test Email',
                message='This is a test email.',
                from_email='chaitanyabardia@gmail.com',
                recipient_list=[email],
                fail_silently=False
            )
            
            successful_emails += 1
            logger.info(f"Successfully sent email to {email}")
            
        except BadHeaderError:
            logger.error(f"Bad header error when sending to {email}")
            failed_emails.append({"email": email, "error": "Bad header error"})
            
        except Exception as e:
            logger.error(f"Failed to send email to {email}: {str(e)}")
            failed_emails.append({"email": email, "error": str(e)})
        
        # Add delay between emails to avoid overwhelming the email server
        sleep(1)

        # Send progress update via WebSocket
        try:
            async_to_sync(channel_layer.group_send)(
                'mail_progress',
                {
                    'type': 'send_email_update',
                    'emails_sent': i + 1,
                    'total_emails': total_emails,
                    'successful_emails': successful_emails,
                    'failed_emails': len(failed_emails),
                    'current_email': email,
                    'status': 'success' if email not in [f['email'] for f in failed_emails] else 'failed'
                }
            )
        except Exception as e:
            logger.error(f"Failed to send WebSocket update: {str(e)}")

        # Update task progress
        self.update_state(
            state='PROGRESS',
            meta={
                'current': i + 1,
                'total': total_emails,
                'successful': successful_emails,
                'failed': len(failed_emails)
            }
        )

    # Send final completion message
    try:
        async_to_sync(channel_layer.group_send)(
            'mail_progress',
            {
                'type': 'send_email_complete',
                'emails_sent': total_emails,
                'total_emails': total_emails,
                'successful_emails': successful_emails,
                'failed_emails': len(failed_emails),
                'failed_list': failed_emails
            }
        )
    except Exception as e:
        logger.error(f"Failed to send completion WebSocket message: {str(e)}")

    logger.info(f"Bulk email task completed. Success: {successful_emails}, Failed: {len(failed_emails)}")
    
    return {
        'total_emails': total_emails,
        'successful_emails': successful_emails,
        'failed_emails': len(failed_emails),
        'failed_list': failed_emails,
        'status': 'completed'
    }