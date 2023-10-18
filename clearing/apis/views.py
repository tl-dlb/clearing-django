from rest_framework import viewsets , status, mixins, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response 

# from accounts.models import User
from clearing.wallets.models import Wallet, Fund
from clearing.apis.serializers import WalletSerializer, FundSerializer, HoldFundSerializer
from clearing.apis.filters import WalletFilter, FundFilter


class WalletView(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer 
    # permission_classes=[IsAuthenticated]
    lookup_field = 'bin'
    filterset_class = WalletFilter
    http_method_names = ['get']

    def retrieve(self, request, bin, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            wallet = queryset.get(trader__bin=bin)
            serializer = self.get_serializer(wallet)
            
            return Response({"wallet": serializer.data})
            
        except Exception:
            return Response({"errors": {
                "body": [
                    "Bad Request"
                ]
            }}, status=status.HTTP_404_NOT_FOUND)     
        


class FundView(viewsets.ModelViewSet):
    queryset = Fund.objects.all()
    serializer_class = FundSerializer 
    # permission_classes=[IsAuthenticated]
    lookup_field = 'id'
    filterset_class = FundFilter
    http_method_names = ['get', 'post', 'delete']

    def get_serializer_class(self):
        if self.action == 'create':
            return HoldFundSerializer
        return FundSerializer

    def create(self, request, *args, **kwargs):
        try:
            input_serializer = HoldFundSerializer(data=request.data)
            input_serializer.is_valid(raise_exception=True)

            wallet = Wallet.objects.get(account_number=input_serializer.data.get('account_number'))
            fund = Fund.objects.create(type='HOLDING', amount=input_serializer.data.get('amount'))
            wallet.funds.add(fund)
            wallet.calculate()

            output_serializer = self.get_serializer(fund)
            headers = self.get_success_headers(output_serializer.data)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception:
            return Response({"errors": {
                "body": [
                    "Bad Request"
                ]
            }}, status=status.HTTP_404_NOT_FOUND)  


    # def retrieve(self, request, bin, *args, **kwargs):
    #     try:
    #         queryset = self.get_queryset()
    #         wallet = queryset.get(trader__bin=bin)
    #         serializer = self.get_serializer(wallet)
            
    #         return Response({"wallet": serializer.data})
            
    #     except Exception:
    #         return Response({"errors": {
    #             "body": [
    #                 "Bad Request"
    #             ]
    #         }}, status=status.HTTP_404_NOT_FOUND)  
        
    
    # @action(detail=True, methods=['post', 'delete'])
    # def hold(self, request, account_number, *args, **kwargs):
    #     if request.method == 'POST':
    #         try:
    #             wallet = Wallet.objects.get(account_number=account_number)
                
                    
    #             serializer = self.get_serializer(wallet)
    #             return Response({"wallet": serializer.data})
                   
    #         except Exception:
    #             return Response({"errors": {
    #                 "body": [
    #                     "Bad Request"
    #                 ]
    #             }}, status=status.HTTP_404_NOT_FOUND) 

       
