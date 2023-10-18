import django_filters 

from clearing.wallets.models import Wallet, Fund


class WalletFilter(django_filters.FilterSet):
    limit = django_filters.NumberFilter(method='limit_filter')
    offset = django_filters.NumberFilter(method='offset_filter')
    
    class Meta:
        model = Wallet
        fields = ['limit', 'offset']
    
    def limit_filter(self, queryset, field_name, value):
        return queryset[:value]
    
    def offset_filter(self, queryset, field_name, value):
        return queryset[value:]
    

class FundFilter(django_filters.FilterSet):
    limit = django_filters.NumberFilter(method='limit_filter')
    offset = django_filters.NumberFilter(method='offset_filter')
    
    class Meta:
        model = Fund
        fields = ['limit', 'offset']
    
    def limit_filter(self, queryset, field_name, value):
        return queryset[:value]
    
    def offset_filter(self, queryset, field_name, value):
        return queryset[value:]