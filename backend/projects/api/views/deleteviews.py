from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import threading

# import models
from projects.models import Pledge, PledgePayment

class deletePayments(APIView):
	'''
		delete an envelope
	'''
	def delete(self, request):
		ids = request.data.get("ids")
		for id in ids:
			payment = PledgePayment.objects.get(id=id)
			payment.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class deletePledges(APIView):
	'''
		delete pledges
	'''
	def delete(self, request):
		ids = request.data.get("ids")
		for id in ids:
			pledge = Pledge.objects.get(id=id)
			pledge.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)