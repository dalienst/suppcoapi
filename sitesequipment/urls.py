from django.urls import path

from sitesequipment.views import (
    SitesEquipmentListCreateView,
    SitesEquipmentRetrieveUpdateDestroyView,
    SitesEquipmentListView,
)

urlpatterns = [
    path(
        "create/",
        SitesEquipmentListCreateView.as_view(),
        name="sites_equipment_list_create",
    ),
    path(
        "<str:reference>/",
        SitesEquipmentRetrieveUpdateDestroyView.as_view(),
        name="sites_equipment_retrieve_update_destroy",
    ),
    path("", SitesEquipmentListView.as_view(), name="sites_equipment_list"),
]
