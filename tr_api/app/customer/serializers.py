from rest_framework_mongoengine import serializers
from django import forms
from tr_api.core.constant import *

from tr_api.app.models import Customer


class CustomerForm(forms.Form):
    uid = forms.CharField(required=False)
    username = forms.CharField(required=True)
    w_type = forms.ChoiceField(choices=[WALLET_TYPE_OPTION], required=True)
    password = forms.CharField(required=False)


class CustomerSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
