from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("companies/", views.company_list, name="company_list"),
    path("companies/search/", views.company_list_search, name="company_list_search"),
    path("companies/create/", views.create_company, name="create_company"),
    path("companies/<uuid:company_id>/", views.company_detail, name="company_detail"),
    path("companies/edit/<uuid:company_id>/", views.edit_company, name="edit_company",),
    path("companies/activate/<uuid:company_id>/", views.invert_company_status, name="invert_company_status"),

    path("companies/<uuid:company_id>/bank_accounts/create/", views.create_bank_accounts, name="create_bank_accounts"),

    
    
    path("history/", views.history, name="history"),
]