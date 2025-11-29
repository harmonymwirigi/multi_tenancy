# from rest_framework import serializers

# from groups.api.serializers import ChurchGroupSerializer
# from member.api.serializers import MemberSerializer
# from member.models import Member
# from sms.models import (Sms, SmsRecipients, SmsRecipientGroups)

# class SmsSerializer(serializers.ModelSerializer):
#     sending_member = MemberSerializer()

#     class Meta:
#         model = Sms
#         fields = ('id', 'app', 'message', 'sending_member',
#                   'date', 'website')
#         depth = 2

#         extra_kwargs = {'id': {'read_only': True}} # dictionary for extra message api, members can only read the message

#     def create(self, validated_data):
#         member_data = validated_data.pop('sending_member')
#         member = {}
#         member = Member.objects.get(member_id=member_data["member"]["id"])

#         sms = Sms.objects.create(sending_member=member, **validated_data)
#         return sms


# class SmsRecipientSerializer(serializers.ModelSerializer):
#     recipient = MemberSerializer()
#     sms = SmsSerializer()

#     class Meta:
#         model = SmsRecipients
#         fields = ('id','sms', 'receipient','cost','status')


# class SmsRecipientGroupsSerializer(serializers.ModelSerializer):
#     recipient_group = ChurchGroupSerializer()
#     sms = SmsSerializer()

#     class Meta:
#         model = SmsRecipientGroups
#         fields = ('sms', 'receipient_group')
#         depth = 1





from rest_framework import serializers
from sms.models import Sms, SmsRecipients
from groups.models import ChurchGroup
from member.models import Member


class SmsSerializer(serializers.ModelSerializer):
    """
    Serializer for the Sms model.
    """
    sending_member = serializers.SerializerMethodField()

    class Meta:
        model = Sms
        fields = ['id', 'tenant', 'app', 'subject', 'message', 'sending_member', 'recipients', 'church_groups', 'date', 'website']
        read_only_fields = ['id', 'date', 'tenant']  #  tenant should be set on creation

    def get_sending_member(self, obj):
        """
        Returns the serialized data of the sending member.
        """
        return MemberSerializer(obj.sending_member).data


class SmsRecipientSerializer(serializers.ModelSerializer):
    """
    Serializer for the SmsRecipient model.
    """
    recipient = serializers.SerializerMethodField()
    sms = serializers.PrimaryKeyRelatedField(queryset=Sms.objects.all()) # changed to PrimaryKeyRelatedField

    class Meta:
        model = SmsRecipients
        fields = ['id', 'sms', 'recipient', 'cost', 'status']
        read_only_fields = ['id', 'cost', 'status']

    def get_recipient(self, obj):
        """
        Returns the serialized data of the recipient.
        """
        return MemberSerializer(obj.recipient).data


class ChurchGroupSerializer(serializers.ModelSerializer):
    """
    Serializer for the ChurchGroup model.
    """

    class Meta:
        model = ChurchGroup
        fields = ['id', 'name', 'description']  # Add other fields as needed


class MemberSerializer(serializers.ModelSerializer):
    """
    Serializer for the Member model.
    """
    first_name = serializers.CharField(source='member.first_name', read_only=True)
    last_name = serializers.CharField(source='member.last_name', read_only=True)
    phone_number = serializers.CharField(source='membercontact.phone', read_only=True)

    class Meta:
        model = Member
        fields = ['id', 'first_name', 'last_name', 'phone_number']  # Add other member fields as needed
