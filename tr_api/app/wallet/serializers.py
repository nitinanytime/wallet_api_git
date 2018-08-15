from rest_framework_mongoengine import serializers
from tr_api.app.models import Transaction, Wallet
from django import forms
from tr_api.core.constant import TYPE_OPTION

class WalletSerializer(serializers.DocumentSerializer):

    class Meta:
        model = Wallet
        fields = '__all__'

class TransactionForm(forms.Form):
    amount = forms.IntegerField(required=True)
    txn_type = forms.ChoiceField(choices=[TYPE_OPTION], required=True)

class TransactionSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

