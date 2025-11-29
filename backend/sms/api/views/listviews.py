# from datetime import date
# from rest_framework import generics
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from sms.models import SmsRecipients
# from sms.api.serializers import SmsRecipientSerializer

# from sms.africastalking.at import ChurchSysMessenger
# from .addviews import CustomMesageFormatter

# today = date.today()
# day = today.day
# month = today.month
# year = today.year

# class SmsList(generics.ListCreateAPIView):
#     '''
#         a list of sms sent this month
#     '''
#     queryset = SmsRecipients.objects.filter(sms__date__year=year,sms__date__month=month).order_by('-sms__date')[:100]
#     serializer_class = SmsRecipientSerializer

# class ExtractCustomMessage(APIView):
#     def get(self,request):
#         message = request.data.get("message")
#         recipient_id = request.data.get("recipient_id")
#         context = request.data.get("context")
#         schema = request.tenant.schema_name
#         message_formatter = CustomMesageFormatter(message,schema,recipient_id,context)
#         return Response(message_formatter.formated_message())

# class SMSCreditBalance(APIView):
#     def get(self,request):
#         schema = request.tenant.schema_name
#         messenger = ChurchSysMessenger(schema)
#         data = messenger.get_sms_credit_balance()

#         return Response(data)



from datetime import date
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from sms.api.views.addviews import CustomMessageFormatter
from django.utils.translation import gettext_lazy as _

from sms.models import SmsRecipients
from sms.api.serializers import SmsRecipientSerializer
from sms.africastalking.at import ChurchSysMessenger  # Import the utility class
import logging

logger = logging.getLogger(__name__)

class SMSException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('SMS service error.')
    default_code = 'sms_error'

class SmsList(generics.ListAPIView):
    """
    A list of SMS sent this month.
    """
    serializer_class = SmsRecipientSerializer

    def get_queryset(self):
        """
        Filter SMS messages for the current month and tenant.
        """
        today = date.today()
        year = today.year
        month = today.month
        tenant = self.request.tenant  # Access the current tenant
        return SmsRecipients.objects.filter(
            sms__tenant=tenant,  # Filter by tenant
            sms__date__year=year,
            sms__date__month=month
        ).order_by('-sms__date')[:100]


class SMSCreditBalanceView(APIView):
    """
    Get the SMS credit balance.
    """
    def get(self, request):
        schema_name = request.tenant.schema_name
        messenger = ChurchSysMessenger(schema_name)
        balance = messenger.get_sms_credit_balance()
        if balance is None:
            raise SMSException(_("Failed to retrieve SMS credit balance."))
        return Response({'balance': balance})


class ExtractCustomMessageView(APIView):
    """
    Extract and format a custom message.
    """
    def get(self, request):
        message = request.query_params.get("message")  # Use query_params for GET
        recipient_id = request.query_params.get("recipient_id")
        context = request.query_params.get("context")
        schema_name = request.tenant.schema_name

        try:
            formatter = CustomMessageFormatter(message, schema_name, recipient_id, context)
            formatted_message = formatter.format_message()
            return Response({'formatted_message': formatted_message})
        except Exception as e:
            logger.exception("Error extracting custom message")
            raise SMSException from e

# class ExtractCustomMessageView(APIView):
#     """
#     Extract and format a custom message.
#     """
#     def get(self, request):
#         message = request.data.get("message")
#         recipient_id = request.data.get("recipient_id")
#         context = request.data.get("context")
#         schema_name = request.tenant.schema_name
#         try:
#             messenger = ChurchSysMessenger(schema_name) #instantiate even if not used
#             message_formatter = messenger.message_formatter #access the default formatter
#             message_formatter = message_formatter.set_message(message) # use the setter
#             message_formatter.set_context(context)
#             message_formatter.set_recipient_id(recipient_id)
#             formatted_message = message_formatter.format_message() # call the format method
#             return Response({'formatted_message': formatted_message})
#         except Exception as e:
#             logger.exception("Error extracting custom message")
#             raise SMSException from e
