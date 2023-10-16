from django.urls import path

from . import views

urlpatterns = [
    path("wallets/<uuid:wallet_id>/create/<slug:fund_type>", views.create_fund, name="create_fund"),

]