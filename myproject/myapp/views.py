# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from myapp.tasks import send_bulk_email
import json

@api_view(["POST"])
def start_sending_email(request):
    """
    Expected payload: {"emails": ["email1@example.com", "email2@example.com"]}
    """
    try:
        emails_list = request.data.get('emails', [])
        
        if not emails_list:
            return Response(
                {"error": "No emails provided.", "success": False}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not isinstance(emails_list, list):
            return Response(
                {"error": "Emails must be provided as a list.", "success": False}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate email format
        valid_emails = []
        for email in emails_list:
            email = email.strip()
            if email and '@' in email:
                valid_emails.append(email)
        
        if not valid_emails:
            return Response(
                {"error": "No valid emails provided.", "success": False}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Start sending emails asynchronously using Celery
        task = send_bulk_email.apply_async(args=[valid_emails])
        
        return Response({
            "success": True,
            "message": "Email sending task started successfully",
            "task_id": task.id,
            "total_emails": len(valid_emails),
            "valid_emails": valid_emails
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {"error": f"An error occurred: {str(e)}", "success": False}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["GET"])
def get_email_status(request):
    """
    API endpoint to get the current status of email sending
    This can be used to check if any email sending is in progress
    """
    try:

        return Response({
            "success": True,
            "message": "Email status retrieved successfully",
            "status": "Use WebSocket connection for real-time updates"
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {"error": f"An error occurred: {str(e)}", "success": False}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["GET"])
def health_check(request):
    """
    API endpoint for health check
    """
    return Response({
        "success": True,
        "message": "Email service is running",
        "status": "healthy"
    }, status=status.HTTP_200_OK)