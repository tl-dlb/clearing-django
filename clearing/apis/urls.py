from django.urls import path, include 
from rest_framework.routers import DefaultRouter

from clearing.apis import views 

wallet_router = DefaultRouter(trailing_slash=False)
wallet_router.register('wallets', views.WalletView, basename='wallets')

fund_router = DefaultRouter(trailing_slash=False)
fund_router.register('funds', views.FundView, basename='funds')

urlpatterns = [
    path('', include(wallet_router.urls)),
    path('', include(fund_router.urls)),
]

