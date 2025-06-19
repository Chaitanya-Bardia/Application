Email Sender API Documentation

Base URL
http://localhost:8000/

API Endpoints
1. Start Sending Emails

Endpoint: POST /api/start-sending-email/

Description: Initiates the bulk email sending process

Request Body:

json{
    "emails": ["user1@example.com", "user2@example.com", "user3@example.com"]
}

Success Response (200):

json{
    "success": true,
    "message": "Email sending task started successfully",
    "task_id": "celery-task-id-here",
    "total_emails": 3,
    "valid_emails": ["user1@example.com", "user2@example.com", "user3@example.com"]
}

Error Response (400):

json{
    "error": "No emails provided.",
    "success": false
}

Error Response (500):

json{
    "error": "An error occurred: error message here",
    "success": false
}

2. Get Email Status

Endpoint: GET /api/email-status/

Description: Get current status of email sending service

Success Response (200):

json{
    "success": true,
    "message": "Email status retrieved successfully",
    "status": "Use WebSocket connection for real-time updates"
}

3. Health Check

Endpoint: GET /api/health/

Description: Check if the email service is running

Success Response (200):

json{
    "success": true,
    "message": "Email service is running",
    "status": "healthy"
}

WebSocket URL

ws://localhost:8000/ws/progress/

WebSocket Message Format

When emails are being sent, you'll receive real-time updates in this format:

json{
    "emails_sent": 2,
    "total_emails": 5
}

Security Notes

CSRF protection is configured

CORS is currently set to allow all origins for development

In production, update CORS_ALLOW_ALL_ORIGINS to False and specify exact origins