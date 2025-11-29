from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime

from member.api.serializers import MemberSerializer
from member.models import Member
from projects.api.serializers import *
from projects.models import Project, Pledge, PendingConfirmation, PledgePayment

from sms.africastalking.at import ChurchSysMessenger
from rest_framework.permissions import IsAuthenticated

class AddPendingConfirmation(APIView):
	'''
		post:
		add pending confirmation
	'''
	def post(self,request):
		project_id = request.data.get("project_id")
		queryset = Project.objects.filter(id=project_id)
		data = []
		for data in queryset:
			data = data
		serializer = ProjectSerializer(data)
		project = serializer.data

		member_id = request.data.get("member_id")
		queryset = Member.objects.filter(member_id=member_id)
		data = []
		for data in queryset:
			data = data
		serializer = MemberSerializer(data)
		member = serializer.data

		confirmation_message = request.data.get("confirmation_message")
		amount = request.data.get("amount")
		type = request.data.get("type")

		data = {'for_project': project, 'confirming_for': member, 'confirmation_message': confirmation_message,
				'amount': amount, 'type': type}

		serializer = PendingConfirmationSerializer(data=data)
		if serializer.is_valid():
			created = serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddContribution(APIView):
	'''
		post:
		add a contribution to a project
	'''

	def post(self, request):

		project_id = request.data.get("project_id")
		queryset = Project.objects.filter(id=project_id)
		data = []
		for data in queryset:
			data = data
		serializer = ProjectSerializer(data)
		project = serializer.data

		member_id = request.data.get("member_id")
		queryset = Member.objects.filter(member_id=member_id)
		data = []
		for data in queryset:
			data = data
		serializer = MemberSerializer(data)
		member = serializer.data

		recording_member_id = request.data.get("recording_member_id")
		queryset = Member.objects.filter(member_id=recording_member_id)
		data = []
		for data in queryset:
			data = data
		serializer = MemberSerializer(data)
		recording_member = serializer.data

		anonymous = request.data.get("anonymous")
		amount = request.data.get("amount")

		data = {'project': project, 'member': member, 'anonymous': anonymous,
				'amount': amount, 'recorded_by': recording_member}

		serializer = AddContributionSerializer(data=data)
		if serializer.is_valid():
			created = serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddAnonymousContribution(APIView):
	'''
		post:
		add an anonymous contribution to a project
	'''

	def post(self, request):

		project_id = request.data.get("project_id")
		queryset = Project.objects.filter(id=project_id)
		data = []
		for data in queryset:
			data = data
		serializer = ProjectSerializer(data)
		project = serializer.data

		recording_member_id = request.data.get("recording_member_id")
		queryset = Member.objects.filter(member_id=recording_member_id)
		data = []
		for data in queryset:
			data = data
		serializer = MemberSerializer(data)
		recording_member = serializer.data

		anonymous = request.data.get("anonymous")
		names = request.data.get("names")
		phone = request.data.get("phone")
		amount = request.data.get("amount")

		data = {'project': project, 'anonymous': anonymous, 'names': names,
				'phone': phone, 'amount': amount, 'recorded_by': recording_member}

		serializer = AddAnonymousContributionSerializer(data=data)
		if serializer.is_valid():
			created = serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddPledge(APIView):
	'''
		post:
		add a pledge by a member to a project
	'''

	def post(self, request):
		project_id = request.data.get("project_id")
		queryset = Project.objects.filter(id=project_id)
		data = []
		for data in queryset:
			data = data
		serializer = ProjectSerializer(data)
		project = serializer.data

		member_id = request.data.get("member_id")
		queryset = Member.objects.filter(member_id=member_id)
		data = []
		for data in queryset:
			data = data
		serializer = MemberSerializer(data)
		member = serializer.data

		recording_member_id = request.data.get("recording_member_id")
		queryset = Member.objects.filter(member_id=recording_member_id)
		data = []
		for data in queryset:
			data = data
		serializer = MemberSerializer(data)
		recording_member = serializer.data

		amount = request.data.get("amount")
		date = request.data.get("date")

		data = {'project': project, 'member': member, 'date': date,
				'amount': amount, 'recorded_by': recording_member}

		serializer = AddPledgeSerializer(data=data)
		if serializer.is_valid():
			created = serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddPledgeAuthenticated(APIView):
	'''
		post:
		add a pledge by a member to a project
	'''
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		project_id = request.data.get("project")
		queryset = Project.objects.filter(id=project_id)
		data = []
		for data in queryset:
			data = data
		serializer = ProjectSerializer(data)
		project = serializer.data

		queryset = Member.objects.filter(member= request.user)
		data = []
		for data in queryset:
			data = data
		serializer = MemberSerializer(data)
		member = serializer.data

		queryset = Member.objects.filter(member= request.user)
		data = []
		for data in queryset:
			data = data
		serializer = MemberSerializer(data)
		recording_member = serializer.data

		amount = request.data.get("amount")
		date = date = datetime.now()
		data = {'project': project, 'member': member, 'date': date,
				'amount': amount, 'recorded_by': recording_member}

		serializer = AddPledgeSerializer(data=data)
		if serializer.is_valid():
			created = serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddAnonymousPledge(APIView):
	'''
		post:
		add a pledge by a non member to a project
	'''

	def post(self, request):
		project_id = request.data.get("project_id")
		queryset = Project.objects.filter(id=project_id)
		data = []
		for data in queryset:
			data = data
		serializer = ProjectSerializer(data)
		project = serializer.data

		recording_member_id = request.data.get("recording_member_id")
		queryset = Member.objects.filter(member_id=recording_member_id)

		data = []
		for data in queryset:
			data = data
		serializer = MemberSerializer(data)
		recording_member = serializer.data

		names = request.data.get("names")
		phone = request.data.get("phone")
		amount = request.data.get("amount")
		date = request.data.get("date")

		data = {'project': project, 'date': date, 'names': names,
				'phone': phone, 'amount': amount, 'recorded_by': recording_member}

		serializer = AddAnonymousPledgeSerializer(data=data)
		if serializer.is_valid():
			created = serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddPledgePayment(APIView):
	'''
		post:
		add a pledge payment by a member to a project
	'''

	def post(self, request):

		project_id = request.data.get("project_id")
		project = Project.objects.get(id=project_id)

		member_id = request.data.get("member_id")
		member = Member.objects.get(member_id=member_id)

		queryset = Pledge.objects.filter(project_id = project.id,
									   member__member__id = member.member.id)
		data = []
		for data in queryset:
			if (data.remaining_amount > 0):
				data = data
				break
		serializer = PledgeSerializer(data)
		pledge = serializer.data

		recording_member_id = request.data.get("recording_member_id")
		queryset = Member.objects.filter(member_id=recording_member_id)
		data = []
		for data in queryset:
			data = data
		serializer = MemberSerializer(data)
		recording_member = serializer.data

		payment_amount = request.data.get("amount")

		data = {'pledge': pledge, 'payment_amount': payment_amount, 'payment_recorded_by': recording_member}

		serializer = PledgePaymentSerializer(data=data)
		if serializer.is_valid():
			created = serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendPledgePaymentReceivedmessage(APIView):
	'''
		post:
		send pledge payment received message
	'''

	def post(self, request):
		schema = request.tenant.schema_name
		messenger = ChurchSysMessenger(schema)
		payment_ids = request.data.get('payment_ids',[])
		for id in payment_ids:
			message = request.data.get('message')
			payment = PledgePayment.objects.get(id=id)
			receipients = messenger.receipients_phone_numbers([payment.pledge.phone])
			if payment.pledge.member:
				message = message.replace("[name]",payment.pledge.member.member.get_full_name())
			else:
				message = message.replace("[name]",payment.pledge.names)
			message = message.replace("[pledged_amount]",str(payment.pledge.amount))
			message = message.replace("[payed_amount]",str(payment.payment_amount))
			message = message.replace("[remaining_amount]",str(payment.remaining_amount))

			member_phone_number = payment.pledge.phone
			if member_phone_number:
				if member_phone_number[0] == '0':
					member_phone_number = member_phone_number.replace('0','+254',1)
				if member_phone_number[:3] == '254':
					member_phone_number = member_phone_number.replace('254','+254',1)
				if len(member_phone_number) == 9:
					member_phone_number = "+254" + member_phone_number			
				messenger.send_message([member_phone_number],message)
				payment.notified = True
				payment.save()
		return Response({"status":"message sent"}, status=status.HTTP_201_CREATED)
