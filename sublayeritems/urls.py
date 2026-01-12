from django.urls import path

from sublayeritems.views import (
    SublayerItemListCreateView,
    SublayerItemListView,
    SublayerItemDetailView,
)

app_name = "sublayeritems"

urlpatterns = [
    path("", SublayerItemListView.as_view(), name="sublayer-item-list"),
    path(
        "list-create/",
        SublayerItemListCreateView.as_view(),
        name="sublayer-item-list-create",
    ),
    path(
        "<str:reference>/",
        SublayerItemDetailView.as_view(),
        name="sublayer-item-detail",
    ),
]
