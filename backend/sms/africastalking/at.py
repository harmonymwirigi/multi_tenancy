# import africastalking
# from decouple import config

# from member.models import MemberContact
# from sms.models import SmsRecipients, Sms
# from Clients.models import Client,ClientDetail, ChurchSMSCredentials
# from django_tenants.utils import schema_context


# '''
# 	this class adapts africastalking api to the sms app.
# '''
# class ChurchSysMesageFormatter():
# 	'''
# 		future proofing so that i can use the class to apply custom formats.
# 		Overide this class' formated_message for custon formats
# 	'''
# 	def __init__(self,message,schema_name):
# 		self.message = message
# 		self.church = Client.objects.get(schema_name=schema_name)

# 	def formatted_message(self):
# 		return  self.message



# class ChurchSysMessenger():
# 	def __init__(self, schema):
# 		self.schema = schema #what schema to use
# 		self.message_formatter = ChurchSysMesageFormatter('blank',self.schema)
# 		self.sender_id = None
# 		username = ''
# 		api_key = ''

# 		# credentials
# 		if schema[slice(0,4)] == "demo":
# 			username = config('DEMO_AFRICAS_TALKING_USERNAME')
# 			api_key = config('DEMO_AFRICAS_TALKING_API_KEY')
# 		else:
# 			credentials = ChurchSMSCredentials.objects.filter(church__schema_name=schema)[0]
# 			username = credentials.at_username
# 			api_key = credentials.at_api_key
# 			if not credentials.at_sender_id == 'AFRICASTKNG':
# 				self.sender_id = credentials.at_sender_id

# 		#initialize africastalking
# 		africastalking.initialize(username, api_key)
# 		self.sms_service = africastalking.SMS
# 		self.balance_service = africastalking.Application

# 	def set_message_formatter(self,message_formatter):
# 		self.message_formatter = message_formatter

# 	def recipients_phone_numbers(self, recipient_member_ids):
# 		'''
# 			get the a list of phone numbers from a list of recipient ids
# 		'''
# 		with schema_context(self.schema):
# 			phone_numbers = []
# 			for data in recipient_member_ids:
# 				try:
# 					contact = MemberContact.objects.filter(member__member__id = data)[0]
# 					member_phone_number = contact.phone
# 					if not member_phone_number:
# 						continue
# 					if member_phone_number[0] == '0':
# 						member_phone_number = member_phone_number.replace('0','+254',1)
# 					if member_phone_number[:3] == '254':
# 						member_phone_number = member_phone_number.replace('254','+254',1)
# 					phone_numbers.append(member_phone_number)
# 				except:
# 					pass #TODO add a mechanism to generate this as a send sms error
# 			return phone_numbers

# 	# def record_members_who_received_sms(self, sent_messages):
# 	#     '''
# 	#         if message was sent, record the members who received it and on what status
# 	#     '''
# 	#     with schema_context(self.schema):
# 	#         for message in sent_messages['SMSMessageData']['Recipients']:
# 	#             try:
# 	#                 contact = MemberContact.objects.filter(phone__contains=message['number'][slice(4,13)])[0]
# 	#                 member = contact.member
# 	#                 sms = Sms.objects.latest('id')
# 	#                 received_sms = SmsRecipients.objects.create(sms=sms, recipient=member, cost=message['cost'], status=message['status'])
# 	#             except MemberContact.DoesNotExist:
# 	#                 pass  
# 	#TODO add a mechanism to generate this as a send sms error

# 	def on_finish(self, error, response):
# 		'''
# 				credentialscallback function called on completion of the thread on which send_message() is running
# 		'''
# 		if error is not None:
# 			raise error

# 	def get_sms_credit_balance(self):

# 		'''
# 			balance inquiry
# 		'''
# 		return self.balance_service.fetch_application_data()

# 	def send_message(self, recipients, message):
# 		'''
# 			send message
# 		'''
# 		sender_id = self.sender_id
# 		formatted_message = self.message_formatter.formatted_message()
# 		if formatted_message == 'blank':
# 			message = message
# 		else:
# 			message = formatted_message
# 		self.sms_service.send(message, recipients, sender_id, callback=self.on_finish)



import africastalking  # Import the Africa's Talking library
from django.conf import settings # Use Django settings instead of decouple
from django.core.exceptions import ObjectDoesNotExist # Import this exception
from member.models import MemberContact  # Import your model
from sms.models import SmsRecipients, Sms  # Import your models
from Clients.models import Client, ClientDetail, ChurchSMSCredentials  # Import your models
from django_tenants.utils import schema_context  # Import for tenant management
import logging

logger = logging.getLogger(__name__) # Initialize logger

'''
    This class adapts Africa's Talking API to the sms app.
'''
class ChurchSysMesageFormatter:
    '''
        Future-proofing so that I can use the class to apply custom formats.
        Override this class's formatted_message for custom formats.
    '''
    def __init__(self, message, schema_name):
        self.message = message
        self.schema_name = schema_name # Changed to schema_name
        self.church = None # Initialize as None
        try:
            with schema_context(self.schema_name): # Moved schema context here
                self.church = Client.objects.get(schema_name=self.schema_name)
        except Client.DoesNotExist:
            logger.error(f"Client with schema '{self.schema_name}' not found.")
            self.church = None

    def formatted_message(self):
        return self.message



# class ChurchSysMessenger:
#     def __init__(self, schema_name):
#         self.schema_name = schema_name  # Changed to schema_name
#         self.message_formatter = ChurchSysMessageFormatter('blank', self.schema_name)
#         self.sender_id = None
#         self.sms_service = None # Initialize as None
#         self.balance_service = None
#         self.username = None
#         self.api_key = None

#         self._initialize_at() #moved to its own method

#     def _initialize_at(self):
#         """Initialize Africa's Talking service."""
#         try:
#             if self.schema_name.startswith("demo"): #check if it is demo
#                 self.username = settings.AFRICASTALKING_USERNAME
#                 self.api_key = settings.AFRICASTALKING_API_KEY
#             else:
#                 with schema_context(self.schema_name):
#                     credentials = ChurchSMSCredentials.objects.get(church__schema_name=self.schema_name) #changed to get
#                     self.username = credentials.at_username
#                     self.api_key = credentials.at_api_key
#                     self.sender_id = credentials.at_sender_id if credentials.at_sender_id != 'AFRICASTKNG' else None
#         except ChurchSMSCredentials.DoesNotExist:
#             logger.error(f"SMS credentials not found for schema '{self.schema_name}'.")
#             # Consider raising an exception or setting default credentials.
#             self.username = settings.AFRICASTALKING_USERNAME
#             self.api_key = settings.AFRICASTALKING_API_KEY

#         # Initialize Africa's Talking
#         if self.username and self.api_key: #check if username and api_key are set
#             africastalking.initialize(self.username, self.api_key)
#             self.sms_service = africastalking.SMS
#             self.balance_service = africastalking.Application
#         else:
#             logger.error(f"Failed to initialize Africa's Talking for schema '{self.schema_name}'")

#     def set_message_formatter(self, message_formatter):
#         self.message_formatter = message_formatter

#     def recipients_phone_numbers(self, recipient_member_ids):
#         '''
#             Get a list of phone numbers from a list of recipient ids.

#             Args:
#                 recipient_member_ids (list): A list of member IDs.

#             Returns:
#                 list: A list of phone numbers.  Empty list if no numbers are found.
#         '''
#         phone_numbers = []
#         if not self.sms_service:
#             logger.error(f"Africas talking not initialized for schema {self.schema_name}")
#             return phone_numbers

#         try:
#             with schema_context(self.schema_name):
#                 contacts = MemberContact.objects.filter(member__id__in=recipient_member_ids) #optimized query
#                 for contact in contacts:
#                     member_phone_number = contact.phone
#                     if not member_phone_number:
#                         logger.warning(f"Member {contact.member.member.id} has no phone number.")
#                         continue
#                     # Clean phone number.
#                     member_phone_number = self._clean_phone_number(member_phone_number)
#                     phone_numbers.append(member_phone_number)
#         except ObjectDoesNotExist as e:
#             logger.error(f"Error fetching recipient phone numbers: {e}")
#         return phone_numbers

#     def _clean_phone_number(self, phone_number):
#         """Clean phone number."""
#         if phone_number[0] == '0':
#             phone_number = phone_number.replace('0', '+254', 1)
#         if phone_number[:3] == '254':
#             phone_number = phone_number.replace('254', '+254', 1)
#         return phone_number

#     def get_sms_credit_balance(self):
#         '''
#             Balance inquiry.

#             Returns:
#                 str: The SMS credit balance, or None on error.
#         '''
#         if not self.balance_service:
#             logger.error(f"Balance service not initialized for schema {self.schema_name}")
#             return None
#         try:
#             response = self.balance_service.fetch_application_data()
#             return response['UserData']['balance']  # Extract the balance
#         except Exception as e:
#             logger.error(f"Error fetching SMS credit balance: {e}")
#             return None

#     def send_message(self, recipients, message):
#         '''
#             Send SMS message.

#             Args:
#                 recipients (list): A list of phone numbers.
#                 message (str): The message to send.

#             Returns:
#                 dict: The response from Africa's Talking, or None on error.
#         '''
#         if not self.sms_service:
#             logger.error(f"SMS service not initialized for schema {self.schema_name}")
#             return None

#         sender_id = self.sender_id
#         formatted_message = self.message_formatter.formatted_message()
#         final_message = formatted_message if formatted_message != 'blank' else message

#         try:
#             response = self.sms_service.send(final_message, recipients, sender_id)
#             return response
#         except Exception as e:
#             logger.error(f"Error sending SMS: {e}")
#             return None

class ChurchSysMessenger:
    def __init__(self, schema_name):
        self.schema_name = schema_name  # Changed to schema_name
        self.message_formatter = ChurchSysMesageFormatter('blank', self.schema_name)
        self.sender_id = None
        self.sms_service = None  # Initialize as None
        self.balance_service = None
        self.username = None
        self.api_key = None

        self._initialize_at()  # moved to its own method

    def _initialize_at(self):
        """Initialize Africa's Talking service."""
        try:
            if self.schema_name.startswith("demo"):  # check if it is demo
                self.username = settings.AFRICASTALKING_USERNAME
                self.api_key = settings.AFRICASTALKING_API_KEY
            else:
                with schema_context(self.schema_name):
                    try:
                        credentials = ChurchSMSCredentials.objects.get(
                            church__schema_name=self.schema_name
                        )  # changed to get
                        self.username = credentials.at_username
                        self.api_key = credentials.at_api_key
                        self.sender_id = (
                            credentials.at_sender_id
                            if credentials.at_sender_id != 'AFRICASTKNG'
                            else None
                        )
                    except ChurchSMSCredentials.DoesNotExist:
                        logger.error(
                            f"SMS credentials not found for schema '{self.schema_name}'."
                        )
                        # Consider raising an exception or setting default credentials.
                        self.username = settings.AFRICASTALKING_USERNAME
                        self.api_key = settings.AFRICASTALKING_API_KEY

        except Exception as e:
            logger.error(
                f"Error initializing Africa's Talking for schema '{self.schema_name}': {e}"
            )
            self.username = settings.AFRICASTALKING_USERNAME
            self.api_key = settings.AFRICASTALKING_API_KEY

        # Initialize Africa's Talking
        if self.username and self.api_key:  # check if username and api_key are set
            africastalking.initialize(self.username, self.api_key)
            self.sms_service = africastalking.SMS
            self.balance_service = africastalking.Application
        else:
            logger.error(
                f"Failed to initialize Africa's Talking for schema '{self.schema_name}'"
            )

    def set_message_formatter(self, message_formatter):
        self.message_formatter = message_formatter

    def recipients_phone_numbers(self, recipient_member_ids):
        '''
            Get a list of phone numbers from a list of recipient ids.

            Args:
                recipient_member_ids (list): A list of member IDs.

            Returns:
                list: A list of phone numbers.  Empty list if no numbers are found.
        '''
        phone_numbers = []
        if not self.sms_service:
            logger.error(
                f"Africas talking not initialized for schema {self.schema_name}"
            )
            return phone_numbers

        try:
            with schema_context(self.schema_name):
                contacts = MemberContact.objects.filter(
                    member__id__in=recipient_member_ids
                )  # optimized query
                for contact in contacts:
                    member_phone_number = contact.phone
                    if not member_phone_number:
                        logger.warning(
                            f"Member {contact.member.member.id} has no phone number."
                        )
                        continue
                    # Clean phone number.
                    member_phone_number = self._clean_phone_number(member_phone_number)
                    phone_numbers.append(member_phone_number)
        except ObjectDoesNotExist as e:
            logger.error(f"Error fetching recipient phone numbers: {e}")
        return phone_numbers

    def _clean_phone_number(self, phone_number):
        """Clean phone number."""
        if phone_number.startswith('0'):
            phone_number = phone_number.replace('0', '+254', 1)
        if phone_number.startswith('254'):
            phone_number = phone_number.replace('254', '+254', 1)
        return phone_number

    def get_sms_credit_balance(self):
        '''
            Balance inquiry.

            Returns:
                str: The SMS credit balance, or None on error.
        '''
        if not self.balance_service:
            logger.error(
                f"Balance service not initialized for schema {self.schema_name}"
            )
            return None
        try:
            response = self.balance_service.fetch_application_data()
            return response['UserData']['balance']  # Extract the balance
        except Exception as e:
            logger.error(f"Error fetching SMS credit balance: {e}")
            return None

    def send_message(self, recipients, message):
        '''
            Send SMS message.

            Args:
                recipients (list): A list of phone numbers.
                message (str): The message to send.

            Returns:
                dict: The response from Africa's Talking, or None on error.
        '''
        if not self.sms_service:
            logger.error(
                f"SMS service not initialized for schema {self.schema_name}"
            )
            return None

        sender_id = self.sender_id
        formatted_message = self.message_formatter.formatted_message()
        final_message = formatted_message if formatted_message != 'blank' else message

        try:
            response = self.sms_service.send(final_message, recipients, sender_id)
            return response
        except Exception as e:
            logger.error(f"Error sending SMS: {e}")
            return {"error": str(e)}  # Return error as part of response