from django.urls import path

from sublayeritems.views import SublayerItemListView, SublayerItemDetailView

app_name = "sublayeritems"

urlpatterns = [
    path("", SublayerItemListView.as_view(), name="sublayer-item-list"),
    path(
        "<str:reference>/",
        SublayerItemDetailView.as_view(),
        name="sublayer-item-detail",
    ),
]
