# Email Sender API

A robust bulk email sending service with real-time progress tracking via WebSocket connections.

## Base URL

```
http://localhost:8000/
```

## API Endpoints

### 1. Start Sending Emails

**Endpoint:** `POST /api/start-sending-email/`

**Description:** Initiates the bulk email sending process

**Request Body:**
```json
{
    "emails": ["user1@example.com", "user2@example.com", "user3@example.com"]
}
```

**Responses:**

**Success Response (200):**
```json
{
    "success": true,
    "message": "Email sending task started successfully",
    "task_id": "celery-task-id-here",
    "total_emails": 3,
    "valid_emails": ["user1@example.com", "user2@example.com", "user3@example.com"]
}
```

**Error Response (400):**
```json
{
    "error": "No emails provided.",
    "success": false
}
```

**Error Response (500):**
```json
{
    "error": "An error occurred: error message here",
    "success": false
}
```

### 2. Get Email Status

**Endpoint:** `GET /api/email-status/`

**Description:** Get current status of email sending service

**Success Response (200):**
```json
{
    "success": true,
    "message": "Email status retrieved successfully",
    "status": "Use WebSocket connection for real-time updates"
}
```

### 3. Health Check

**Endpoint:** `GET /api/health/`

**Description:** Check if the email service is running

**Success Response (200):**
```json
{
    "success": true,
    "message": "Email service is running",
    "status": "healthy"
}
```

## WebSocket Connection

### WebSocket URL
```
ws://localhost:8000/ws/progress/
```

### Real-time Updates

When emails are being sent, you'll receive real-time progress updates in this format:

```json
{
    "emails_sent": 2,
    "total_emails": 5
}
```

## Usage Example

### Starting Email Sending

```bash
curl -X POST http://localhost:8000/api/start-sending-email/ \
  -H "Content-Type: application/json" \
  -d '{
    "emails": [
      "user1@example.com",
      "user2@example.com",
      "user3@example.com"
    ]
  }'
```

### Health Check

```bash
curl http://localhost:8000/api/health/
```

### WebSocket Connection (JavaScript)

```javascript
const socket = new WebSocket('ws://localhost:8000/ws/progress/');

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log(`Progress: ${data.emails_sent}/${data.total_emails} emails sent`);
};

socket.onopen = function(event) {
    console.log('WebSocket connection established');
};

socket.onclose = function(event) {
    console.log('WebSocket connection closed');
};
```

## Security Configuration

- **CSRF Protection:** Configured and enabled
- **CORS:** Currently set to allow all origins for development purposes
- **Production Note:** Update `CORS_ALLOW_ALL_ORIGINS` to `False` and specify exact allowed origins in production

## Development Setup

1. Ensure the service is running on `localhost:8000`
2. Use the health check endpoint to verify service status
3. Connect to WebSocket for real-time progress updates
4. Send POST requests to start email sending tasks

## Error Handling

The API returns appropriate HTTP status codes:
- **200:** Success
- **400:** Bad Request (invalid input)
- **500:** Internal Server Error

All error responses include a descriptive error message and `success: false` flag.

## Features

- ✅ Bulk email sending
- ✅ Real-time progress tracking via WebSocket
- ✅ Email validation
- ✅ Task ID tracking
- ✅ Health monitoring
- ✅ CSRF protection
- ✅ CORS configuration

## Support

For issues or questions, please check the service logs or contact the development team.