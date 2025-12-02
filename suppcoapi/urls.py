from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("accounts.urls")),
    path("api/v1/companies/", include("companies.urls")),
    path("api/v1/roles/", include("roles.urls")),
    path("api/v1/branches/", include("branches.urls")),
    path("api/v1/sites/", include("sites.urls")),
    path("api/v1/employees/", include("employment.urls")),
    # Inventory
    path("api/v1/layers/", include("layers.urls")),
    path("api/v1/sublayers/", include("sublayers.urls")),
    path("api/v1/sublayeritems/", include("sublayeritems.urls")),
    path("api/v1/brackets/", include("brackets.urls")),
    path("api/v1/shellequipment/", include("shellequipment.urls")),
]
