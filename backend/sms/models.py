
from django.db import models
from datetime import datetime


from django.conf import settings

from groups.models import ChurchGroup
from member.models import Member


class Sms(models.Model):
    '''
        sms sent by the church are logged here
    '''
    id = models.AutoField(primary_key=True)
    tenants = models.ForeignKey(settings.TENANT_MODEL, on_delete=models.CASCADE, default=1)
    app = models.CharField(max_length=160, help_text='the app this message was sent from', default="admin")
    subject = models.CharField(max_length=200, blank=True,null=True)
    message = models.CharField(max_length=160, )
    sending_member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='sending_member')
    recipients = models.ManyToManyField(Member, through='SmsRecipients', related_name = 'sms_messages')
    church_groups = models.ManyToManyField(ChurchGroup, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    website = models.BooleanField(default=True, help_text='Publish on the website')

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('-date',)
        permissions = [
            ('can_send_sms', 'can send SMS messages' ),
        ]


class SmsRecipients(models.Model):
    '''
        who received the message and on what status
    '''
    sms = models.ForeignKey(Sms, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='recipient')
    cost = models.CharField(max_length=20, default="0")
    status = models.CharField(max_length=100, default="0")
    
    class Meta:
        unique_together = ('sms', 'recipient')



class SmsRecipientGroups(models.Model):
    '''
        what groups will receive the message
    '''
    sms = models.ForeignKey(Sms, on_delete=models.CASCADE)
    recipient_group = models.ForeignKey(Sms, on_delete=models.CASCADE, related_name='sms_recipient_group')

    class Meta:
        unique_together = ('sms', 'recipient_group')
