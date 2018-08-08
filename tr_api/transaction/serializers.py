from rest_framework_mongoengine import serializers

from tr_api.transaction.models import Transaction, Wallet, Customer


class TransactionSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class CustomerSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Customer
        fields = '__all__'



class WalletSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'