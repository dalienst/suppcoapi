from django.urls import path

from layers.views import LayerListCreateView, LayerDetailView

app_name = "layers"

urlpatterns = [
    path("", LayerListCreateView.as_view(), name="layer-list"),
    path("<str:reference>/", LayerDetailView.as_view(), name="layer-detail"),
]
