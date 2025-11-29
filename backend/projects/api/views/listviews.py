from datetime import date,timedelta

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from projects.api.serializers import *
from projects.models import (Project, Contribution, Pledge, PledgePayment, PendingConfirmation)
from django.core.paginator import Paginator

class PendingConfirmations(generics.ListCreateAPIView):
	'''
		get:
		get the list of all pending confirmations
	'''
	queryset = PendingConfirmation.objects.all()
	serializer_class = PendingConfirmationSerializer

class ConfirmPayment(APIView):
	'''
		get:
		confirm a pending confirmation
	'''
	def get(self, request, pending_confirmation_id):
		data = {}
		pending_confirmation = PendingConfirmation.objects.get(id=pending_confirmation_id)
		confirmed = pending_confirmation.confirmPayment()
		if (pending_confirmation.type == "C"):
			data = ContributionSerializer(confirmed, many=True).data
		else:
			data = PledgePaymentSerializer(confirmed, many=True).data
		return Response(data)

class ProjectList(generics.ListCreateAPIView):
	'''
		get:
		a list of Projects
		post:
		add a project
	'''
	queryset = Project.objects.all().order_by('-start')
	serializer_class = ProjectSerializer


class ProjectWithID(APIView):
	'''
		get:
		get project with id <id>
	'''

	def get(self, request, id):
		project = Project.objects.filter(id=id)
		data = ProjectSerializer(project, many=True).data
		return Response(data)


class ContributionsForAProject(APIView):
	'''
		get:
		contributions made by members for a project with id <id>
	'''

	def get(self, request, id):
		contribution = Contribution.objects.filter(project_id=id).order_by('-recorded_at')[:100]
		data = ContributionSerializer(contribution, many=True).data
		return Response(data)


class ContributionsByAMember(APIView):
	'''
		get:
		contributions made by member with id <id>
	'''

	def get(self, request, id):
		contribution = Contribution.objects.filter(member__member_id=id).order_by('-recorded_at')[:50]
		data = ContributionSerializer(contribution, many=True).data
		return Response(data)


class PledgesForAProject(APIView):
	'''
		get:
		pledges made by members for a project with id <id>
	'''

	def get(self, request, id):
		page = request.GET.get('p',1)
		pledge = Pledge.objects.filter(project_id=id).order_by('-recorded_at')
		data = PledgeSerializer(pledge, many=True).data
		paginator = Paginator(data,20)
		data = paginator.page(page)
		data = data.object_list
		res = Response({"data":data,"page_count":paginator.num_pages})
		return res


class PledgesByAmember(APIView):
	'''
		get:
		pledges made by member with id <id>
	'''

	def get(self, request, id):
		pledge = Pledge.objects.filter(member__member_id=id)[:50]
		data = PledgeSerializer(pledge, many=True).data
		return Response(data)


class PledgePaymentForAProject(APIView):
	'''
		get:
		pledges payment made by members for a project with id <id>
	'''

	def get(self, request, id):
		today = date.today() + timedelta(days=1)
		pre_month = date(today.year, today.month, 1) - timedelta(days=1)
		pre_month = pre_month.replace(day=1)
		from_date = request.GET.get('from_date',pre_month)
		to_date = request.GET.get('to_date',today)		
		pledge_payment = PledgePayment.objects.filter(
			pledge__project_id=id,
			payment_recorded_on__gte=from_date,
			payment_recorded_on__lte=to_date,
		).order_by('-payment_recorded_on')
		data = PledgePaymentSerializer(pledge_payment, many=True).data
		return Response(data)


class PledgePaymentForAMember(APIView):
	'''
		get:
		pledges payments made by member with id <id> for project with id <project_id>
	'''

	def get(self, request, id, project_id):
		pledge_payment = PledgePayment.objects.filter(pledge__project_id=project_id, pledge__member__member_id=id)[:50]
		data = PledgePaymentSerializer(pledge_payment, many=True).data
		return Response(data)
