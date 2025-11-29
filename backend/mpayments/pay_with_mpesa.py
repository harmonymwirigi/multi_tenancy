import json
from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from finance.models import ModeOfPayment,Offering,OfferingType,Tithe,PaymentIntent
from projects.models import PledgePayment,Pledge
from member.models import Member
from finance.api.serializers import OfferingSerializer
from .daraja import STKPush

class payWithMpesa(APIView):
	'''
		settle finances with MPESA
		types:offering,tithe,pledge_payment,contribution
	'''
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		phonenumber = request.data.get("phonenumber")
		type = request.data.get("type")
		id = request.data.get("id",None)
		amount = request.data.get('amount')
		member = Member.objects.get(member= request.user)

		response = STKPush(int(phonenumber),amount,"t-" + str(member.id))
		response_text = response.text
		response_json = json.loads(response_text)

		if 'errorCode' in response_json:
			data = {'errors': [response_json['errorMessage']]}
			return Response(data, status=status.HTTP_400_BAD_REQUEST)
		checkout_request_id = response_json['CheckoutRequestID']
		intent = PaymentIntent.objects.create(
			member = member,
			type = type,
			amount =  amount,
			reference = checkout_request_id,
			project_id = id if type == "Pledge" else None,
			offering_type_id = id if type == "Offering" else None
		)
		intent.save()
		return Response({"status":"payment is being processed"}, status=status.HTTP_201_CREATED)

class STKPushCallback(APIView):
	def get_status(self, data):
		try:
			status = data["Body"]["stkCallback"]["ResultCode"]
		except Exception as e:
			status = 1
		return status

	def get_intent_object(self, data):
		checkout_request_id = data["Body"]["stkCallback"]["CheckoutRequestID"]
		intent, _ = PaymentIntent.objects.get_or_create(
			reference=checkout_request_id
		)
		return intent

	def handle_successful_pay(self, data, intent):
		items = data["Body"]["stkCallback"]["CallbackMetadata"]["Item"]
		description = data["Body"]["stkCallback"]["ResultDesc"]

		for item in items:
			if item["Name"] == "Amount":
				amount = item["Value"]
			elif item["Name"] == "MpesaReceiptNumber":
				receipt_no = item["Value"]
			elif item["Name"] == "PhoneNumber":
				phone_number = item["Value"]

		if intent.type == "Tithe":
			tithe = Tithe.objects.create(
				amount = amount,
				member = intent.member,
				date = datetime.now(),
			)
			tithe.save()
			intent.confirmed = True
			intent.save()
		if intent.type == "Pledge":
			payment = PledgePayment.objects.create(
				payment_amount=amount,
				pledge=Pledge.objects.get(id=intent.project_id),
				payment_recorded_on= datetime.now(),
				payment_recorded_by= intent.member
			)
			payment.save()
			intent.confirmed = True
			intent.save()

		if intent.type == "Offering":
			mode_of_payment,created = ModeOfPayment.objects.get_or_create(name="mpesa")
			offering = Offering.objects.create(
				type = OfferingType.objects.get(id=intent.offering_type_id),
				amount = amount,
				mode_of_payment = mode_of_payment,
				member = intent.member,
				recorded_by = intent.member,
				date = datetime.now()
			)
			offering.save()
			intent.confirmed = True
			intent.save()
		return

	def callback_handler(self, data):
		status = self.get_status(data)
		intent = self.get_intent_object(data)
		if status==0:
			self.handle_successful_pay(data, intent)
		else:
			description = data["Body"]["stkCallback"]["ResultDesc"]
			intent.description = description
		intent.save()

		return Response({"status": "ok", "code": 0}, status=200)

	def get(self, request):
		return Response({"status": "OK"}, status=200)

	def post(self, request):
		data = request.data
		self.callback_handler(data)
		return self.callback_handler(data)

class confirmPayments(APIView):
	'''
		receives response from safaricom
	'''
	def post(self, request):
		print(request.data,"confirm payments")
		return Response({"status":"done"}, status=status.HTTP_201_CREATED)

class validatePayments(APIView):
	'''
		receives response from safaricom
	'''
	def post(self, request):
		print(request.data,'validate payments')
		return Response({"status":"done"}, status=status.HTTP_201_CREATED)
