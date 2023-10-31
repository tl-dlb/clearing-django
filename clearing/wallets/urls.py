from django.urls import path

from . import views

urlpatterns = [
    path("wallets/<uuid:wallet_id>/create/<slug:fund_type>", views.create_io_fund, name="create_fund"),

    path("wallets/<uuid:wallet_id>/", views.io_fund_list, name="io_fund_list"),
    path("wallets/<uuid:wallet_id>/search/", views.io_fund_list_search, name="io_fund_list_search"),
    
    path("wallets/<uuid:wallet_id>/holding/", views.holding_fund_list, name="holding_fund_list"),
    path("wallets/<uuid:wallet_id>/holding/search/", views.holding_fund_list_search, name="holding_fund_list_search"),

    path("wallets/<uuid:wallet_id>/locked/", views.locked_fund_list, name="locked_fund_list"),
    path("wallets/<uuid:wallet_id>/locked/search/", views.locked_fund_list_search, name="locked_fund_list_search"),

    path("wallets/<uuid:wallet_id>/funds/invert_status/<uuid:fund_id>/", views.invert_fund_status, name="invert_fund_status"),
]