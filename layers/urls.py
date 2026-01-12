from django.urls import path

from layers.views import LayerListCreateView, LayerDetailView, LayerListView

app_name = "layers"

urlpatterns = [
    path("", LayerListView.as_view(), name="layer-list"),
    path("list-create/", LayerListCreateView.as_view(), name="layer-list-create"),
    path("<str:reference>/", LayerDetailView.as_view(), name="layer-detail"),
]
