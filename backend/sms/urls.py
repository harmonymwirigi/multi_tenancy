from django.urls import path
from . import views

app_name = 'sms'
urlpatterns = [
    path('send/', views.send_sms_view, name='send_sms'),
    # path('send/process/', views.SendSMSProcessView.as_view(), name='send_sms_process'),
]