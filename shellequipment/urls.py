from django.urls import path

from shellequipment.views import (
    ShellEquipmentListCreateView,
    ShellEquipmentListView,
    ShellEquipmentRetrieveUpdateDestroyView,
)

app_name = "shellequipment"
urlpatterns = [
    path("", ShellEquipmentListView.as_view(), name="shell_equipment_list"),
    path(
        "create/", ShellEquipmentListCreateView.as_view(), name="shell_equipment_create"
    ),
    path(
        "<str:reference>/",
        ShellEquipmentRetrieveUpdateDestroyView.as_view(),
        name="shell_equipment_retrieve_update_destroy",
    ),
]
