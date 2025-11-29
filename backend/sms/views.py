# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required, permission_required
# from django.views import View
# from groups.models import ChurchGroup
# from member.models import Member
# from sms.africastalking.at import ChurchSysMessenger
# from django.contrib import messages
# from .models import Sms

# @login_required
# @permission_required("sms.can_send_sms", raise_exception=True)
# def send_sms_view(request):
#     church_groups = ChurchGroup.objects.filter(tenant=request.tenant)
#     members = Member.objects.filter(tenant=request.tenant).select_related('member', 'membercontact', 'churchgroup')
#     context = {
#         'church_groups': church_groups,
#         'members': members,
#     }
#     return render(request, 'sms/send_sms.html', context)

# class SendSMSProcessView(View):
#     @login_required
#     @permission_required("sms.can_send_sms", raise_exception=True)
#     def post(self, request):
#         subject = request.POST.get('subject', '')
#         message = request.POST.get('message')
#         recipient_ids = request.POST.getlist('recipients')

#         if not message:
#             messages.error(request, "Please enter a message to send.")
#             return redirect('sms:send_sms')

#         if not recipient_ids:
#             messages.warning(request, "Please select at least one recipient.")
#             return redirect('sms:send_sms')

#         tenant = request.tenant
#         messenger = ChurchSysMessenger(tenant.schema_name)
#         members = Member.objects.using(tenant.schema_name).filter(id__in=recipient_ids).select_related('membercontact')
#         phone_numbers = [member.membercontact.phone for member in members if member.membercontact and member.membercontact.phone]

#         if not phone_numbers:
#             messages.warning(request, "No valid phone numbers found for the selected recipients.")
#             return redirect('sms:send_sms')

#         try:
#             response = messenger.send_message(phone_numbers, message)
#             if response and response.get('SMSMessageData') and response['SMSMessageData'].get('Recipients'):
#                 sent_count = len([r for r in response['SMSMessageData']['Recipients'] if r['status'] == 'Success'])
#                 Sms.objects.create(
#                     tenant=tenant,
#                     sender=request.user.member,  # Assuming User has a related Member
#                     subject=subject,
#                     message=message,
#                 )
#                 messages.success(request, f"{sent_count} SMS messages sent successfully.")
#             else:
#                 messages.error(request, "Failed to send SMS messages.")
#         except Exception as e:
#             messages.error(request, f"An error occurred while sending SMS: {e}")

#         return redirect('sms:send_sms')


# # from django.shortcuts import render
# # from django.contrib.auth.decorators import login_required, permission_required
# # from groups.models import ChurchGroup
# # from member.models import Member

# # @login_required
# # @permission_required("sms.can_send_sms", raise_exception=True)
# # def send_sms_view(request):
# #     # Assuming GroupOfChurchGroups has a 'tenant' field
# #     church_groups = ChurchGroup.objects.filter(group__tenant=request.tenant)
# #     members = Member.objects.filter(churchgroup__group__tenant=request.tenant).select_related('member', 'membercontact', 'churchgroup')
# #     context = {
# #         'church_groups': church_groups,
# #         'members': members,
# #     }
# #     return render(request, 'sms/send_sms.html', context)

# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required, permission_required
# from django.views import View
# from groups.models import ChurchGroup
# from member.models import Member
# from sms.africastalking.at import ChurchSysMessenger
# from django.contrib import messages
# from .models import Sms

# @login_required
# @permission_required("sms.can_send_sms", raise_exception=True)
# def send_sms_view(request):
#     church_groups = ChurchGroup.objects.filter(group__tenant=request.tenant) # Corrected line
#     members = Member.objects.filter(churchgroup__group__tenant=request.tenant).select_related('member', 'membercontact', 'churchgroup') # Corrected line
#     context = {
#         'church_groups': church_groups,
#         'members': members,
#     }
#     return render(request, 'sms/send_sms.html', context)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from groups.models import ChurchGroup, GroupOfChurchGroups # Import GroupOfChurchGroups
from member.models import Member
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from groups.models import ChurchGroup, GroupOfChurchGroups # Import GroupOfChurchGroups
from member.models import Member
from django.views import View
from sms.africastalking.at import ChurchSysMessenger
from django.contrib import messages
from .models import Sms

@login_required
@permission_required("sms.can_send_sms", raise_exception=True)
def send_sms_view(request):
    # Get the GroupOfChurchGroups instance for the current tenant
    try:
        group_of_church_groups = GroupOfChurchGroups.objects.get(name=request.tenant.name) #Assumes the group name is the same as the tenant name.
    except GroupOfChurchGroups.DoesNotExist:
        # Handle the case where the GroupOfChurchGroups instance doesn't exist for this tenant.
        #  You might want to log an error or show a message to the user.
        church_groups = ChurchGroup.objects.none()  # Return empty queryset
        members = Member.objects.none()            # Return empty queryset
        messages.error(request, "No Church Groups found for this tenant.")

    else:
        # Filter ChurchGroups and Members using the GroupOfChurchGroups instance
        church_groups = ChurchGroup.objects.filter(group=group_of_church_groups)
        members = Member.objects.filter(churchgroup__group=group_of_church_groups).select_related('member', 'membercontact', 'churchgroup')

    context = {
        'church_groups': church_groups,
        'members': members,
    }
    return render(request, 'sms/send_sms.html', context)
from sms.africastalking.at import ChurchSysMessenger
from django.contrib import messages
from .models import Sms

# @login_required
# @permission_required("sms.can_send_sms", raise_exception=True)
# def send_sms_view(request):
#     # Get the GroupOfChurchGroups instance for the current tenant
#     try:
#         group_of_church_groups = GroupOfChurchGroups.objects.get(name=request.tenant.name) #Assumes the group name is the same as the tenant name.
#     except GroupOfChurchGroups.DoesNotExist:
#         # Handle the case where the GroupOfChurchGroups instance doesn't exist for this tenant.
#         #  You might want to log an error or show a message to the user.
#         church_groups = ChurchGroup.objects.none()  # Return empty queryset
#         members = Member.objects.none()            # Return empty queryset
#         messages.error(request, "No Church Groups found for this tenant.")

#     else:
#         # Filter ChurchGroups and Members using the GroupOfChurchGroups instance
#         church_groups = ChurchGroup.objects.filter(group=group_of_church_groups)
#         members = Member.objects.filter(churchgroup__group=group_of_church_groups).select_related('member', 'membercontact', 'churchgroup')

#     context = {
#         'church_groups': church_groups,
#         'members': members,
#     }
#     return render(request, 'sms/send_sms.html', context)
@login_required
@permission_required("sms.can_send_sms", raise_exception=True)
def send_sms_view(request):
     # Get the GroupOfChurchGroups instance for the current tenant
    try:
        # Assuming that you have a way to get the GroupOfChurchGroups instance for a tenant.
        # You might have a field in GroupOfChurchGroups that links it to the tenant.
        #  If the tenant name is the same as the group name, then the below should work.
        group_of_church_groups = GroupOfChurchGroups.objects.get(name=request.tenant.name)
    except GroupOfChurchGroups.DoesNotExist:
        # Handle the case where the GroupOfChurchGroups instance doesn't exist for this tenant.
        #  You might want to log an error or show a message to the user.
        church_groups = ChurchGroup.objects.none()  # Return empty queryset
        members = Member.objects.none()            # Return empty queryset
        messages.error(request, "No Church Groups found for this tenant.")  #  Import messages
    else:
        # Filter ChurchGroups and Members using the GroupOfChurchGroups instance
        church_groups = ChurchGroup.objects.filter(group=group_of_church_groups)
        # members = Member.objects.filter(churchgroup__group=group_of_church_groups).select_related('member', 'membercontact', 'churchgroup')
        members = Member.objects.all().select_related('member','membercontact','churchgroup')

    context = {
        'church_groups': church_groups,
        'members': members,
        # 'member': member,
    }
    return render(request, 'sms/send_sms.html', context)

# class SendSMSProcessView(View):
#     @login_required
#     @permission_required("sms.can_send_sms", raise_exception=True)
#     def post(self, request):
#         subject = request.POST.get('subject', '')
#         message = request.POST.get('message')
#         recipient_ids = request.POST.getlist('recipients')

#         if not message:
#             messages.error(request, "Please enter a message to send.")
#             return redirect('sms:send_sms')

#         if not recipient_ids:
#             messages.warning(request, "Please select at least one recipient.")
#             return redirect('sms:send_sms')

#         tenant = request.tenant
#         messenger = ChurchSysMessenger(tenant.schema_name)
#         members = Member.objects.using(tenant.schema_name).filter(id__in=recipient_ids).select_related('membercontact')
#         phone_numbers = [member.membercontact.phone for member in members if member.membercontact and member.membercontact.phone]

#         if not phone_numbers:
#             messages.warning(request, "No valid phone numbers found for the selected recipients.")
#             return redirect('sms:send_sms')

#         try:
#             response = messenger.send_message(phone_numbers, message)
#             if response and response.get('SMSMessageData') and response['SMSMessageData'].get('Recipients'):
#                 sent_count = len([r for r in response['SMSMessageData']['Recipients'] if r['status'] == 'Success'])
#                 Sms.objects.create(
#                     tenant=tenant,
#                     sender=request.user.member,  # Assuming User has a related Member
#                     subject=subject,
#                     message=message,
#                 )
#                 messages.success(request, f"{sent_count} SMS messages sent successfully.")
#             else:
#                 messages.error(request, "Failed to send SMS messages.")
#         except Exception as e:
#             messages.error(request, f"An error occurred while sending SMS: {e}")

#         return redirect('sms:send_sms')

class SendSMSProcessView(View):
    @login_required
    @permission_required("sms.can_send_sms", raise_exception=True)
    def post(self, request):
        subject = request.POST.get('subject', '')
        message = request.POST.get('message')
        recipient_ids = request.POST.getlist('recipients')

        if not message:
            messages.error(request, "Please enter a message to send.")
            return redirect('sms:send_sms')

        if not recipient_ids:
            messages.warning(request, "Please select at least one recipient.")
            return redirect('sms:send_sms')

        tenant = request.tenant
        messenger = ChurchSysMessenger(tenant.schema_name)
        members = Member.objects.using(tenant.schema_name).filter(
            id__in=recipient_ids
        ).select_related('membercontact')
        phone_numbers = [
            member.membercontact.phone
            for member in members
            if member.membercontact and member.membercontact.phone
        ]

        if not phone_numbers:
            messages.warning(
                request, "No valid phone numbers found for the selected recipients."
            )
            return redirect('sms:send_sms')

        try:
            response = messenger.send_message(phone_numbers, message)
            if response and response.get('SMSMessageData') and response['SMSMessageData'].get('Recipients'):
                successful_recipients = [
                    r for r in response['SMSMessageData']['Recipients'] if r['status'] == 'Success'
                ]
                sent_count = len(successful_recipients)
                Sms.objects.create(
                    tenant=tenant,
                    sender=request.user.member,  # Assuming User has a related Member
                    subject=subject,
                    message=message,
                )
                messages.success(
                    request, f"{sent_count} SMS messages sent successfully."
                )
            else:
                messages.error(request, "Failed to send SMS messages.")
        except Exception as e:
            messages.error(request, f"An error occurred while sending SMS: {e}")

        return redirect('sms:send_sms')