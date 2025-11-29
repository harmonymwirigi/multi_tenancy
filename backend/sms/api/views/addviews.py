# from django.contrib.humanize.templatetags.humanize import intcomma
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from member.api.serializers import MemberSerializer
# from member.models import Member
# from finance.models import Tithe,Offering
# from projects.models import Pledge,Contribution

# from sms.africastalking.at import ChurchSysMessenger,ChurchSysMesageFormatter
# from sms.api.serializers import SmsSerializer

# def getSerializerData(queryset,serializer_class):
# 	serializer = serializer_class(queryset[0])
# 	return serializer.data


# class MesageFormatter(ChurchSysMesageFormatter):
# 	'''
# 		how this message is formated
# 	'''
# 	def formated_message(self):
# 		return  self.message # + "\n" + self.church.domain_ur

# class CustomMesageFormatter(ChurchSysMesageFormatter):
# 	'''
# 		for sending custom messages after recording member finances
# 	'''
# 	def __init__(self,message,schema_name,id,context):
# 		super().__init__(message,schema_name)#initialize message and schema_name
# 		self.member = None
# 		self.first_name = None
# 		self.this_amount = ''
# 		self.this_date = ''
# 		self.recent_giving = ''
# 		self.this_type = ''
# 		if context == "All":
# 			if (id['type'] == "Tithe"):
# 				try:
# 					tithe = Tithe.objects.get(id=id['id'])
# 					tithe.notified = True
# 					tithe.save()
# 					self.member = tithe.member
# 					self.this_amount = tithe.amount
# 					self.this_date = tithe.date
# 					self.this_type = "Tithe"
# 					self.recent_giving = "total this month is : " + str(tithe.total_this_month) + ", " +\
# 					"total this year is : " + str(tithe.total_this_month)
# 				except Tithe.DoesNotExist:
# 					pass
# 			else:
# 				try:
# 					offering = Offering.objects.get(id=id['id'])
# 					offering.notified = True
# 					offering.save()
# 					self.member = offering.member
# 					self.this_amount = offering.amount
# 					self.this_date = offering.date
# 					if offering.type:
# 						self.this_type = offering.type.name
# 					self.recent_giving = "total this month is : " + str(offering.total_this_month) + ", " +\
# 					"total this year is : " + str(offering.total_this_month)
# 				except Offering.DoesNotExist:
# 					pass

# 		if context == "Tithe":
# 			try:
# 				tithe = Tithe.objects.get(id=id)
# 				tithe.notified = True
# 				tithe.save()
# 				self.member = tithe.member
# 				self.this_amount = tithe.amount
# 				self.this_date = tithe.date
# 				self.this_type = "Tithe"
# 				self.recent_giving = "total this month is : " + str(tithe.total_this_month) + ", " +\
# 				"total this year is : " + str(tithe.total_this_month)
# 			except Tithe.DoesNotExist:
# 				print("passed")
# 				pass

# 		if context == "Offering":
# 				try:
# 					offering = Offering.objects.get(id=id)
# 					offering.notified = True
# 					offering.save()
# 					self.member = offering.member
# 					self.this_amount = offering.amount
# 					self.this_date = offering.date
# 					if offering.type:
# 						self.this_type = offering.type.name
# 					self.recent_giving = "total this month is : " + str(offering.total_this_month) + ", " +\
# 					"total this year is : " + str(offering.total_this_month)
# 				except Offering.DoesNotExist:
# 					pass

# 		if context == "Pledge":
# 			pledge = Pledge.objects.filter(member_id=id).latest('id')
# 			self.this_amount =  str(pledge.amount) + " towards project " + pledge.project.name
# 			self.this_date = str(pledge.date)
# 			self.recent_giving = "amount so far is " + str(pledge.amount_so_far) + ", "+\
# 			"remaining amount is "+ str(pledge.remaining_amount) + " (" + str(pledge.percentage_funded) +")"

# 		if context == "Contribution":
# 			contribution = Contribution.objects.filter(member_id=id).latest('id')
# 			self.this_amount =  str(contribution.amount) + " towards project " + contribution.project.name
# 			self.this_date = str(contribution.recorded_at)

# 		self.replace_with_member_data()


# 	def replace_with_member_data(self):
# 		'''
# 			replace data in '[]' with appropriate member data
# 		'''
# 		if self.member:
# 			self.message = self.message.replace("[name]",self.member.member.get_full_name())
# 		self.message = self.message.replace("[amount]",intcomma(int(self.this_amount)))
# 		self.message = self.message.replace("[date]",self.this_date.strftime("%d/%b/%y"))
# 		self.message = self.message.replace("[type]",self.this_type)

# 		#capital letters
# 		if self.member:
# 			self.message = self.message.replace("[Name]",self.member.member.get_full_name())
# 		self.message = self.message.replace("[Amount]",intcomma(int(self.this_amount)))
# 		self.message = self.message.replace("[Date]",self.this_date.strftime("%d/%b/%y"))
# 		self.message = self.message.replace("[Type]",self.this_type)

# 	def formated_message(self):
# 		return  self.message #+   "\n\n" + self.church.domain_url

# 	def member_id(self):
# 		return self.member.member.id

# class addSMS(APIView):
# 	'''
# 		add sms
# 	'''

# 	def post(self, request):

# 		sending_member_id = request.data.get("sending_member_id")
# 		app = request.data.get("app")
# 		message = request.data.get("message")
# 		website = request.data.get("website")
# 		receipient_member_ids = request.data.get("receipient_member_ids")

# 		schema = request.tenant.schema_name
# 		message_formatter = MesageFormatter(message,schema)

# 		messenger = ChurchSysMessenger(schema)
# 		messenger.set_message_formatter(message_formatter)
# 		receipients = messenger.receipients_phone_numbers(receipient_member_ids)
# 		messenger.send_message(receipients,message)

# 		queryset = Member.objects.filter(member_id=sending_member_id)
# 		sending_member = getSerializerData(queryset,MemberSerializer)

# 		data = {'sending_member': sending_member, 'app': app, 'message': message, 'website': website}
# 		serializer = SmsSerializer(data=data)
# 		if serializer.is_valid():
# 			created = serializer.save()
# 			return Response(serializer.data, status=status.HTTP_201_CREATED)
# 		else:
# 			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class addCustomSMS(APIView):
# 	'''
# 		custom sms for every member it is sent to
# 	'''

# 	def post(self, request):
# 		sending_member_id = request.data.get("sending_member_id")
# 		app = request.data.get("app")
# 		message = request.data.get("message")
# 		website = request.data.get("website")
# 		context = request.data.get("context")
# 		receipient_member_ids = request.data.get("receipient_member_ids")

# 		schema = request.tenant.schema_name
# 		messenger = ChurchSysMessenger(schema)
# 		try:
# 			for id in receipient_member_ids:
# 				#create a message formater.
# 				message_formatter = CustomMesageFormatter(message,schema,id,context)
# 				if message_formatter.member:
# 					messenger.set_message_formatter(message_formatter)
# 					receipient = messenger.receipients_phone_numbers([message_formatter.member_id()])
# 					if len(receipient):						
# 						messenger.send_message(receipient,message_formatter.formated_message())

# 			return Response(status=status.HTTP_204_NO_CONTENT)
# 		except:
# 			return Response(status=status.HTTP_400_BAD_REQUEST)


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _
from django.db import transaction

from member.api.serializers import MemberSerializer
from member.models import Member
from finance.models import Tithe, Offering
from projects.models import Pledge, Contribution
from sms.africastalking.at import ChurchSysMessenger, ChurchSysMesageFormatter  # Import the utility and the base formatter
from sms.api.serializers import SmsSerializer
import logging

logger = logging.getLogger(__name__)

class SMSException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('SMS service error.')
    default_code = 'sms_error'


class CustomMessageFormatter(ChurchSysMesageFormatter): #rename
    """
    Formats custom messages for various financial transactions.
    """

    def __init__(self, message, schema_name, recipient_id, context):
        super().__init__(message, schema_name)  # Initialize message and schema_name
        self.recipient_id = recipient_id
        self.context = context
        self.member = None
        self.this_amount = ''
        self.this_date = ''
        self.recent_giving = ''
        self.this_type = ''
        self._get_transaction_details()  # Get transaction details

    def _get_transaction_details(self):
        """
        Retrieves transaction details based on the context (Tithe, Offering, etc.).
        """
        transaction_model = None
        try:
            if self.context == "All":
                if self.recipient_id['type'] == "Tithe":
                    transaction_model = Tithe
                    transaction = Tithe.objects.get(id=self.recipient_id['id'])
                    self.this_type = "Tithe"
                else:
                    transaction_model = Offering
                    transaction = Offering.objects.get(id=self.recipient_id['id'])
                    if transaction.type:
                        self.this_type = transaction.type.name
            elif self.context == "Tithe":
                transaction_model = Tithe
                transaction = Tithe.objects.get(id=self.recipient_id)
                self.this_type = "Tithe"
            elif self.context == "Offering":
                transaction_model = Offering
                transaction = Offering.objects.get(id=self.recipient_id)
                if transaction.type:
                    self.this_type = transaction.type.name
            elif self.context == "Pledge":
                transaction_model = Pledge
                transaction = Pledge.objects.filter(member_id=self.recipient_id).latest('id')
            elif self.context == "Contribution":
                transaction_model = Contribution
                transaction = Contribution.objects.filter(member_id=self.recipient_id).latest('id')

            if transaction_model: # None check
                if self.context in ["Tithe", "Offering", "All"]:
                    transaction.notified = True
                    transaction.save()
                    self.member = transaction.member
                    self.this_amount = transaction.amount
                    self.this_date = transaction.date
                    self.recent_giving = "total this month is : " + str(
                        transaction.total_this_month) + ", " + \
                                        "total this year is : " + str(transaction.total_this_month)
                elif self.context == "Pledge":
                    self.member = transaction.member
                    self.this_amount = str(transaction.amount) + " towards project " + transaction.project.name
                    self.this_date = str(transaction.date)
                    self.recent_giving = "amount so far is " + str(
                        transaction.amount_so_far) + ", " + \
                                            "remaining amount is " + str(
                        transaction.remaining_amount) + " (" + str(
                        transaction.percentage_funded) + ")"
                elif self.context == "Contribution":
                    self.member = transaction.member
                    self.this_amount = str(
                        transaction.amount) + " towards project " + transaction.project.name
                    self.this_date = str(transaction.recorded_at)
        except transaction_model.DoesNotExist: # type: ignore
            logger.warning(f"{transaction_model.__name__} with id {self.recipient_id} not found.") # type: ignore

    def format_message(self):
        """
        Formats the message with member-specific data.
        """
        formatted_message = self.message
        if self.member:
            formatted_message = formatted_message.replace("[name]", self.member.get_full_name())
            formatted_message = formatted_message.replace("[Name]", self.member.get_full_name())
        formatted_message = formatted_message.replace("[amount]", intcomma(int(self.this_amount)) if self.this_amount else "")
        formatted_message = formatted_message.replace("[Amount]", intcomma(int(self.this_amount))  if self.this_amount else "")
        formatted_message = formatted_message.replace("[date]", self.this_date.strftime("%d/%b/%y") if self.this_date else "")
        formatted_message = formatted_message.replace("[Date]", self.this_date.strftime("%d/%b/%y") if self.this_date else "")
        formatted_message = formatted_message.replace("[type]", self.this_type) if self.this_type else ""
        formatted_message = formatted_message.replace("[Type]", self.this_type) if self.this_type else ""
        return formatted_message #+   "\n\n" + self.church.domain_url  removed church

    def get_member_id(self): #chnaged name
        return self.member.id if self.member else None

class SendSMSView(APIView): #changed name
    """
    Add SMS.
    """

    def post(self, request):
        sending_member_id = request.data.get("sending_member_id")
        app = request.data.get("app")
        message = request.data.get("message")
        website = request.data.get("website")
        recipient_member_ids = request.data.get("recipient_member_ids")

        schema_name = request.tenant.schema_name

        try:
            messenger = ChurchSysMessenger(schema_name)
            message_formatter = ChurchSysMessageFormatter(message, schema_name) # default formatter
            messenger.set_message_formatter(message_formatter)
            recipients = messenger.recipients_phone_numbers(recipient_member_ids)
            if not recipients:
                return Response({"message": "No valid phone numbers found for recipients."},
                                status=status.HTTP_200_OK)  # Or 400?
            response = messenger.send_message(recipients, message)
            if response is None:
                raise SMSException(_("Failed to send SMS message."))

            with transaction.atomic():
                sender_member = Member.objects.get(id=sending_member_id) # changed to get
                sms_data = {'sending_member': sender_member, 'app': app, 'message': message, 'website': website, 'tenant': request.tenant}
                serializer = SmsSerializer(data=sms_data)
                serializer.is_valid(raise_exception=True)
                created_sms = serializer.save()

                # Create SmsRecipient entries
                for recipient_id in recipient_member_ids:
                    recipient_member = Member.objects.get(id=recipient_id)
                    SmsRecipient.objects.create(sms=created_sms, recipient=recipient_member,
                                                status=response['SMSMessageData']['Messages'][0]['status'])  # Adjust as needed

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception("Error adding and sending SMS")
            raise SMSException from e



class SendCustomSMSView(APIView): #changed name
    """
    Send custom SMS for every member it is sent to.
    """

    def post(self, request):
        sending_member_id = request.data.get("sending_member_id")
        app = request.data.get("app")
        message = request.data.get("message")
        website = request.data.get("website")
        context = request.data.get("context")
        recipient_member_ids = request.data.get("recipient_member_ids")

        schema_name = request.tenant.schema_name
        try:
            messenger = ChurchSysMessenger(schema_name)
            with transaction.atomic():
                for recipient_id in recipient_member_ids:
                    # Create a message formatter.
                    message_formatter = CustomMessageFormatter(message, schema_name, recipient_id, context)
                    member_id = message_formatter.get_member_id()
                    if member_id:  #check if member is None
                        recipient_phone_numbers = messenger.recipients_phone_numbers([member_id])
                        if recipient_phone_numbers:
                            response = messenger.send_message(recipient_phone_numbers,
                                                            message_formatter.format_message())
                            if response:
                                # Create SMS and SmsRecipient
                                sender_member = Member.objects.get(id=sending_member_id)
                                sms_data = {'sending_member': sender_member, 'app': app, 'message': message,
                                            'website': website, 'tenant': request.tenant}
                                serializer = SmsSerializer(data=sms_data)
                                serializer.is_valid(raise_exception=True)
                                created_sms = serializer.save()
                                SmsRecipient.objects.create(sms=created_sms, recipient_id=member_id,
                                                            status=response['SMSMessageData']['Messages'][0]['status'])
                            else:
                                logger.warning(f"Failed to send sms to member {member_id}")

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.exception("Error sending custom SMS")
            raise SMSException from e