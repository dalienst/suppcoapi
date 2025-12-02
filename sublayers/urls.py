from django.urls import path

from sublayers.views import SubLayerListCreateView, SubLayerRetrieveUpdateDestroyView

app_name = "sublayers"

urlpatterns = [
    path("", SubLayerListCreateView.as_view(), name="sublayer-list-create"),
    path(
        "<str:reference>/",
        SubLayerRetrieveUpdateDestroyView.as_view(),
        name="sublayer-retrieve-update-destroy",
    ),
]
