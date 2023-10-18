from datetime import datetime
from rest_framework import serializers

from clearing.wallets.models import Wallet, Fund


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['account_number', 'currency_code', 'deposited_amount', 'holding_amount', 'locked_amount', 'available_amount']
        read_only_fields = ['account_number', 'currency_code', 'deposited_amount', 'holding_amount', 'locked_amount', 'available_amount']


class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = ['id', 'type', 'amount', 'is_active']


class HoldFundSerializer(serializers.Serializer):
    platform = serializers.CharField()
    account_number = serializers.CharField()   
    amount = serializers.DecimalField(max_digits=32, decimal_places=2)


class FreeFundSerializer(serializers.Serializer):
    account_number = serializers.CharField()  
    id = serializers.UUIDField()   


class LockFundSerializer(serializers.Serializer):
    account_number = serializers.CharField()  
    id = serializers.UUIDField()   