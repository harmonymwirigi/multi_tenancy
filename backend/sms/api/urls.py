from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import addviews,listviews

# TODO add delete views
urlpatterns = [

    path('sms-this-month/', listviews.SmsList.as_view()),
    path('extract-custom-message/',listviews.ExtractCustomMessageView.as_view()),
    path('sms-credit-balance/',listviews.SMSCreditBalanceView.as_view()),

    #add
    path('add-sms/', addviews.SendSMSView.as_view()),
    path('add-custom-sms/', addviews.SendCustomSMSView.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
