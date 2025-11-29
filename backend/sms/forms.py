from django import forms
from member.models import Member
from groups.models import ChurchGroup
from django.forms import CheckboxSelectMultiple


class SendSMSForm(forms.Form):
    subject = forms.CharField(label='Subject',required=False, widgets=forms.TextInput(attrs={'class': 'form-control','rows': 4}))
    message = forms.CharField(label = 'message',widget = forms.Textarea(attr={'class': 'form-control','rows': 4}))
    recipients = forms.ModelMultipleChoiceField(queryset = Member.objects.all(), widget=form.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}), label='select members')
    groups = form.ModelMultipleChoiceField(queryset=ChurchGroup.objects.all(), widget=CheckboxSelectMultiple(attrs={'class':'form-check-input'}), required=False, label = 'Select Groups')


    def __init__(self, *args, **kwargs):
        tenant = kwargs.pop('tenant',None)
        super().__init__(*args, **kwargs)
        if tenant:
            self.fields['recipients'].queryset=Member.objects.using(tenant.schema_name).all()
            self.fields['groups'].queryset=ChurchGroup.objects.using(tenant.schema_name).all() #filter groups by tenant
            


