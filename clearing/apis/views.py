from rest_framework import viewsets , status, mixins, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response 

# from accounts.models import User
from clearing.wallets.models import Wallet, Fund
from clearing.apis import serializers
from clearing.apis.filters import WalletFilter, FundFilter


class WalletView(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = serializers.WalletSerializer 
    # permission_classes=[IsAuthenticated]
    lookup_field = 'bin'
    filterset_class = WalletFilter
    http_method_names = ['get']

    def retrieve(self, request, bin, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            wallet = queryset.get(trader__bin=bin)
            serializer = self.get_serializer(wallet)
            
            return Response(serializer.data)
            
        except Exception:
            return Response({"errors": {
                "body": [
                    "Bad Request"
                ]
            }}, status=status.HTTP_404_NOT_FOUND)     
        


class FundView(viewsets.ModelViewSet):
    queryset = Fund.objects.all()
    serializer_class = serializers.FundSerializer 
    # permission_classes=[IsAuthenticated]
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'delete']

    def get_serializer_class(self):

        if self.action == 'hold':
            return serializers.HoldFundSerializer
        if self.action == 'free':
            return serializers.FreeFundSerializer
        if self.action == 'lock':
            return serializers.LockFundSerializer
        return serializers.FundSerializer

    def hold(self, request, *args, **kwargs):
        
        input_serializer = serializers.HoldFundSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            wallet = Wallet.objects.get(account_number=input_serializer.data.get('account_number'))
        except Exception:
            return Response({"errors": {
                "body": [
                    "Invalid account number"
                ]
            }}, status=status.HTTP_404_NOT_FOUND)  
        
        if (amount := float(input_serializer.data.get('amount'))) > wallet.available_amount:
            return Response({"errors": {
                "body": [
                    "Invalid amount to hold"
                ]
            }}, status=status.HTTP_404_NOT_FOUND)  


        fund = Fund.objects.create(
            platform=input_serializer.data.get('platform'),
            type='HOLDING', 
            amount=amount,
            comment=input_serializer.data.get('comment'),
        )
        wallet.funds.add(fund)
        wallet.calculate()

        output_serializer = serializers.FundSerializer(fund)
        headers = self.get_success_headers(output_serializer.data)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    
        
    def free(self, request, *args, **kwargs):

        input_serializer = serializers.FreeFundSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            wallet = Wallet.objects.get(account_number=input_serializer.data.get('account_number'))
        except Exception:
            return Response({"errors": {
                "body": [
                    "Invalid account number"
                ]
            }}, status=status.HTTP_404_NOT_FOUND)  

        try:
            holding_fund = Fund.objects.get(id=input_serializer.data.get('id'))
        except Exception:
            return Response({"errors": {
                "body": [
                    "Invalid fund id"
                ]
            }}, status=status.HTTP_404_NOT_FOUND)  
       
        holding_fund.is_active = False
        holding_fund.save()
        wallet.calculate()

        output_serializer = serializers.FundSerializer(holding_fund)
        headers = self.get_success_headers(output_serializer.data)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    
    def lock(self, request, *args, **kwargs):

        input_serializer = serializers.LockFundSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            wallet = Wallet.objects.get(account_number=input_serializer.data.get('account_number'))
        except Exception:
            return Response({"errors": {
                "body": [
                    "Invalid account number"
                ]
            }}, status=status.HTTP_404_NOT_FOUND)  

        try:
            holding_fund = Fund.objects.get(id=input_serializer.data.get('id'))
        except Exception:
            return Response({"errors": {
                "body": [
                    "Invalid fund id"
                ]
            }}, status=status.HTTP_404_NOT_FOUND)  
       
        holding_fund.is_active = False
        holding_fund.save()

        locked_fund = Fund.objects.create(
            platform=holding_fund.platform,
            type='LOCKED', 
            amount=holding_fund.amount,
            comment=input_serializer.data.get('comment'),
        )

        wallet.funds.add(locked_fund)
        wallet.calculate()

        output_serializer = serializers.FundSerializer(locked_fund)
        headers = self.get_success_headers(output_serializer.data)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
