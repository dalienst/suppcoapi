from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("accounts.urls")),
    path("api/v1/companies/", include("companies.urls")),
    path("api/v1/roles/", include("roles.urls")),
    path("api/v1/branches/", include("branches.urls")),
    path("api/v1/sites/", include("sites.urls")),
]
