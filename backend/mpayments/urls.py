from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns

from .pay_with_mpesa import payWithMpesa,confirmPayments, validatePayments, STKPushCallback

urlpatterns = [
    path('pay-with-mpesa/', payWithMpesa.as_view()),
	path('acknowledge-payments/',STKPushCallback.as_view()),
	path('confirmation/', confirmPayments.as_view()),
	path('validation/', validatePayments.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
