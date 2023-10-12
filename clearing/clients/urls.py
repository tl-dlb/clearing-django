from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("clients/", views.client_list, name="client_list"),
    path("clients/search/", views.client_list_search, name="client_list_search"),
    path("clients/create/", views.create_client, name="create_client"),
    path("clients/<uuid:client_id>/", views.client_detail, name="client_detail"),
    path("clients/edit/<uuid:client_id>/", views.edit_client, name="edit_client",),
    path("clients/activate/<uuid:client_id>/", views.activate_client, name="activate_client"),

    path("clients/<uuid:client_id>/bank_accounts/create/", views.create_bank_accounts, name="create_bank_accounts"),

    
    
    path("history/", views.history, name="history"),
]