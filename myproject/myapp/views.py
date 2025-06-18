from django.shortcuts import render
from django.http import JsonResponse
from .tasks import send_bulk_email
import json

def home(request):
    return render(request, 'home.html')

def start_sending_email(request):
    # Get emails from the POST request
    emails = request.body.decode('utf-8')
    
    # Receive the list of emails
    emails_list = json.loads(emails).get('emails') 
    
    # Parse emails from the body
    if not emails_list:
        return JsonResponse({"error": "No emails provided."}, status=400)

    # Start sending emails asynchronously using Celery
    send_bulk_email.apply_async(args=[emails_list])

    # Return response indicating the task is started
    return JsonResponse({"status": "Mail sending task started"})

def count_page(request):
    return render(request, 'count_page.html', {'total_emails': 0}) #initially no mails sent,hence we will pass 0 in total mails
