from django.urls import path
from myapp import views
from myapp.views import health_check,get_email_status,start_sending_email

urlpatterns = [
    path('api/start-sending-email/',start_sending_email, name='api_start_sending_email'),
    path('api/email-status/',get_email_status, name='api_email_status'),
    path('api/health/',health_check, name='api_health_check'),
]

