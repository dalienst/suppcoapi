from django.urls import path

from sublayers.views import (
    SubLayerListCreateView,
    SubLayerRetrieveUpdateDestroyView,
    SubLayerListView,
)

app_name = "sublayers"

urlpatterns = [
    path("", SubLayerListView.as_view(), name="sublayer-list"),
    path("list-create/", SubLayerListCreateView.as_view(), name="sublayer-list-create"),
    path(
        "<str:reference>/",
        SubLayerRetrieveUpdateDestroyView.as_view(),
        name="sublayer-retrieve-update-destroy",
    ),
]
