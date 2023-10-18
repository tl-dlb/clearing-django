from django.urls import path

from . import views

urlpatterns = [
    path("wallets/<uuid:wallet_id>/", views.fund_list, name="fund_list"),
    path("wallets/<uuid:wallet_id>/search/", views.fund_list_search, name="fund_list_search"),
    path("wallets/<uuid:wallet_id>/create/<slug:fund_type>", views.create_fund, name="create_fund"),

]