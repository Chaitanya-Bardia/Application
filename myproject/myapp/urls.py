from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('start-sending-email/', views.start_sending_email, name='start_sending_email'),
    path('count-page/', views.count_page, name='count_page'),
]

