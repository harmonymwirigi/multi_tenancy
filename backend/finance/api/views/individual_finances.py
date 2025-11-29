from datetime import datetime
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db.models import Sum

from finance.api.serializers import *
from finance.models import *

class MemberTithes(APIView):
	'''
		get tithes
	'''
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		params = dict(request.GET)
		user = request.user
		if not len(params):
			#tithes
			tithe = Tithe.objects.filter(member__member=user).order_by('-date')[:100]
			data = TitheSerializer(tithe, many=True).data
			data.sort(reverse=True,key = lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
			return Response(data)
		else:
			# tithes
			tithe = Tithe.objects.filter(
				member__member=user,
				date__gte=params['from_date'][0],
				date__lte=params['to_date'][0]
			).order_by('-date')
			data = TitheSerializer(tithe, many=True).data
			data.sort(reverse=True,key = lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
			return Response(data)

class MemberOfferings(APIView):
	'''
		get both tithes and offerings
	'''
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		user = request.user
		params = dict(request.GET)
		type_id = request.GET.get('offering_type')
		data = []
		if len(params) < 2:
			#offerings
			offering = Offering.objects.filter(member__member=user,type_id=type_id).order_by('-timestamp')
			data += OfferingSerializer(offering, many=True).data

			data.sort(reverse=True,key = lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
			return Response(data)
		if len(params) == 3:
			#offerings
			offerings = Offering.objects.filter(
				member__member=user,
				type_id=type_id,
				date__gte=params['from_date'][0],
				date__lte=params['to_date'][0]
			).order_by('-date')
			data += OfferingSerializer(offerings, many=True).data
			data.sort(reverse=True,key = lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
			return Response(data)


class TitheStats(APIView):
	'''
		statistics for tithes this month and this year
	'''
	permission_classes = (IsAuthenticated,)

	def get(self, request):
		user = request.user
		stat_dict = {}
		if request.GET.get('from_date') == None and request.GET.get('to_date') == None:
			stat_dict["total"] = Tithe.objects.filter(
				member__member=user
			).aggregate(Sum('amount'))['amount__sum'] or 0
		else:
			stat_dict["total"] = Tithe.objects.filter(
				member__member=user,
				date__gte=request.GET.get('from_date'),
				date__lte=request.GET.get('to_date')
			).aggregate(Sum('amount'))['amount__sum'] or 0
		return Response(stat_dict)


class OfferingStats(APIView):
	'''
		statistics for offerings this month.
	'''
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		type_id = request.GET.get('offering_type')
		user = request.user
		stat_dict = {}
		if request.GET.get('from_date') == None and request.GET.get('to_date') == None:
			stat_dict["total"] = Offering.objects.filter(
				member__member=user,
				type_id=type_id
			).aggregate(Sum('amount'))['amount__sum'] or 0

		else:
			stat_dict["total"] = Offering.objects.filter(
				member__member=user,
				type_id=type_id,
				date__gte=request.GET.get('from_date'),
				date__lte=request.GET.get('to_date')
			).aggregate(Sum('amount'))['amount__sum'] or 0

		return Response(stat_dict)
