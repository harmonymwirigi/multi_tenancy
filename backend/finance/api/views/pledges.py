from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser

#import serializers
from finance.api.serializers import *
from member.api.serializers import MemberSerializer
# import models
from finance.models import *
from member.models import Member
from services.models import Service,ServiceType
#import from CSV
from finance.resources.importPledgesFromCSV import CSVLoader
csv_loader = CSVLoader()

def getSerializerData(queryset,serializer_class):
	if len(queryset) == 0:
		return None
	data = queryset[0]
	return serializer_class(data).data


class UploadCSV(APIView):
	'''
		post:
		upload a csv file, check if the file is of valid type and format
	'''
	parser_class = (FileUploadParser,)

	def post(self, request, *args, **kwargs):

	  csv_loader.set_base_url(request.get_host())
	  file_serializer = CSVFileSerializer(data=request.data)

	  if file_serializer.is_valid():
		  file_serializer.save()

		  return Response(file_serializer.data, status=status.HTTP_201_CREATED)
	  else:
		  return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PreviewCSV(APIView):
	'''
		get:
		get csv data for preview in the UI
	'''

	def get(self, request, file_id):
		path = CSV.objects.get(id=file_id).csv.path
		data = csv_loader.preview_CSV(path)
		return Response(data)

class CheckCSV(APIView):
	'''
		post:
		check that the csv file sent has no
	'''

	def post(self, request):
			csv_loader.set_base_url(request.get_host())
			file_id = request.data.get('file_id')
			column_config = request.data.get('column_config')
			file_path = CSV.objects.get(id=file_id).csv.path

			try:
				csv_loader.configure_CSV(file_path,column_config)
				csv_loader.check_CSV(file_path)
				if (csv_loader.errors):
					errors = csv_loader.errors
					if len(errors) > 5:
						#get only the first 5 errors
						errors.insert( 5, " + "
										+ str((len(errors)-5))
										+ " similar errors")

					errors = errors[:6]
					return Response(errors)
			except:
				return Response(status=status.HTTP_400_BAD_REQUEST)
			else:
				return Response(status=status.HTTP_201_CREATED)

class ImportDataFromCsv(APIView):
	'''
		post:
		import data from a csv file given the name
	'''

	def post(self, request):
			file_id = request.data.get('file_id')
			column_config = request.data.get('column_config')
			file_path = CSV.objects.get(id=file_id).csv.path

			schema = request.tenant.schema_name
			csv_loader.configure_CSV(file_path,column_config)

			try:
				csv_loader.add_pledge_payments(schema,file_path)
			except:
				return Response(status=status.HTTP_400_BAD_REQUEST)
			else:
				CSV.objects.get(id=file_id).delete()
				return Response(status=status.HTTP_201_CREATED)
