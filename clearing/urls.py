from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("clearing.companies.urls")),
    path("", include("clearing.wallets.urls")),
    # path("admin/", admin.site.urls),
]
