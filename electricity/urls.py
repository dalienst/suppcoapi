from django.urls import path

from electricity.views import (
    ElectricityListCreateView,
    ElectricityRetrieveUpdateDestroyView,
    ElectricityListView,
)

app_name = "electricity"

urlpatterns = [
    path(
        "create/",
        ElectricityListCreateView.as_view(),
        name="electricity-list-create",
    ),
    path(
        "<str:reference>/",
        ElectricityRetrieveUpdateDestroyView.as_view(),
        name="electricity-retrieve-update-destroy",
    ),
    path("", ElectricityListView.as_view(), name="electricity-list"),
]
