from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser

from groups.api.serializers import *
from groups.models import ChurchGroup, ChurchGroupMembership
from member.models import Member, Role

from groups.api.serializers import  *
from member.api.serializers import RoleSerializer,MemberSerializer

from groups.resources.importFromCSV import CSVLoader
from sms.africastalking.at import ChurchSysMessenger,ChurchSysMesageFormatter
csv_loader = CSVLoader()

def getSerializerData(queryset,serializer_class):
    data = queryset[0]
    return serializer_class(data).data

class AddGroup(APIView):
    '''
    post:
    add a group
    '''
    def post(self,request):
        serializer = ChurchGroupSerializer(data=request.data,partial=True)

        if serializer.is_valid():
            created = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddMemberToGroup(APIView):
    '''
        post:
        add a member to a group
    '''

    def post(self, request):
        data = request.data
        data['member'] = Member.objects.get(member_id=data['member']).id
        if data['role'] == None:
            data['role'] = Role.objects.get_or_create(role='member')[0].id
        serializer = ChurchGroupMembershipSerializer(data=data,partial=True)
        if serializer.is_valid():
            created = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BulkAddMembersToGroup(APIView):
    '''
        post:
        add a member to a group
    '''

    def post(self, request):
        group_id = request.data.get("group_id")
        member_ids = request.data.get("member_ids")
        role_id = request.data.get("role_id")

        for id in member_ids:
            if ChurchGroupMembership.objects.filter(member__member_id=id,church_group_id=group_id).first():#if member
                pass
            else:
                try:
                    member  = Member.objects.get(member_id=id)
                    group = ChurchGroup.objects.get(id=group_id)
                    role = Role.objects.get_or_create(role="member")[0]
                    ChurchGroupMembership.objects.create(church_group=group,member = member,role=role)
                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            return Response(status=status.HTTP_201_CREATED)

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
        file_path = CSV.objects.get(id=file_id).csv.path
        data = csv_loader.preview_CSV(file_path)
        return Response(data)

class CheckCSV(APIView):
    '''
        post:
        check that the csv file sent has no
    '''

    def post(self, request):
        
        file_id = request.data.get('file_id')
        file_path = CSV.objects.get(id=file_id).csv.path
        column_config = request.data.get('column_config')

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

class MesageFormatter(ChurchSysMesageFormatter):
    '''
        how this message is formated
    '''
    def formated_message(self):
        return  self.message

class SendMessageToNumbersInCsv(APIView):
    '''
        post:
        import data from a csv file given the name
    '''

    def post(self, request):
        file_id = request.data.get('file_id')
        file_path = CSV.objects.get(id=file_id).csv.path
        column_config = request.data.get('column_config')
        message = request.data.get("message")
       
        csv_loader.configure_CSV(file_path,column_config)
        schema = request.tenant.schema_name
        messenger = ChurchSysMessenger(schema)           

        try:            
            for phone_number,names in csv_loader.get_phone_numbers(file_path):            
                msg = message.replace("[name]",names)                              
                messenger.send_message([phone_number],msg)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_201_CREATED)
