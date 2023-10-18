from django.urls import path, include 
from rest_framework.routers import DefaultRouter

from clearing.apis import views 

wallet_detail = views.WalletView.as_view({'get': 'retrieve'})
fund_hold = views.FundView.as_view({'post': 'hold'})
fund_free = views.FundView.as_view({'post': 'free'})
fund_lock = views.FundView.as_view({'post': 'lock'})


urlpatterns = [
    path('wallets/<str:bin>/', wallet_detail, name='wallet-detail'),
    path('funds/hold', fund_hold, name='fund-hold'),
    path('funds/free', fund_free, name='fund-lock'),
    path('funds/lock', fund_lock, name='fund-lock'),
]

