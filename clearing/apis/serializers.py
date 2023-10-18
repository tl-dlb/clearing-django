from datetime import datetime
from rest_framework import serializers

from clearing.wallets.models import Wallet, Fund


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['account_number', 'currency_code', 'deposited_amount', 'holding_amount', 'locked_amount', 'available_amount']
        read_only_fields = ['account_number', 'currency_code', 'deposited_amount', 'holding_amount', 'locked_amount', 'available_amount']


class FundSerializer(serializers.ModelSerializer):
    # account_number = serializers.CharField()
    class Meta:
        model = Fund
        fields = ['type', 'amount', 'id']
        # read_only_fields = ['account_number']

class HoldFundSerializer(serializers.Serializer):
    account_number = serializers.CharField()   
    type = serializers.CharField()  
    amount = serializers.DecimalField(max_digits=32, decimal_places=2)