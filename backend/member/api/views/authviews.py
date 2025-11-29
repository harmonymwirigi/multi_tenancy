import math, random
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from member.models import Member,MemberContact,OTP

from rest_framework_simplejwt.tokens import RefreshToken
from sms.africastalking.at import ChurchSysMessenger,ChurchSysMesageFormatter

class MesageFormatter(ChurchSysMesageFormatter):
	'''
		how this message is formated
	'''
	def formated_message(self):
		return  self.message # + "\n" + self.church.domain_ur

class GenerateOTP(APIView):

	def post(self,request):
		phone_number = request.data.get('phone_number')
		phone_number = phone_number[-9:]#get the last 9 digits
		# check if user with phone number exits
		contact = MemberContact.objects.filter(phone__contains=phone_number)
		if not len(contact):
			return Response("member with that contact doest not exist", status=status.HTTP_400_BAD_REQUEST)
		else:
			# print(contact[0])
			#generate OTP
			# which stores all digits
			digits = "0123456789"
			code = ""
			# length of password can be chaged
			# by changing value in range
			for i in range(6) :
				code += digits[math.floor(random.random() * 10)]
			#get timestamp
			otp =  OTP.objects.create(code=code,member=contact[0].member)
			# print(otp,otp.code)
			# send OTP
			message = "Your OTP code is " + otp.code
			schema = request.tenant.schema_name
			message_formatter = MesageFormatter(message,schema)
			messenger = ChurchSysMessenger(schema)
			messenger.set_message_formatter(message_formatter)
			recipients = messenger.receipients_phone_numbers([contact[0].member.member.id])
			messenger.send_message(recipients,message)
			return Response("OTP generated", status=status.HTTP_201_CREATED)

class LoginWithOTP(APIView):
	def post(self,request):
		code = request.data.get('code')
		otp = None
		try:
			otp = OTP.objects.get(code=code)
		except:
			return Response("OTP does not exist or has already been used", status=status.HTTP_400_BAD_REQUEST)
		user = otp.member.member
		refresh = RefreshToken.for_user(user)
		data = {
			"new_user": False,
			"refresh": str(refresh),
			"access": str(refresh.access_token),
			"username": user.username,
			"full_name":user.get_full_name()
		}
		otp.delete()
		return Response(data)
