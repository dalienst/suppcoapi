from django.urls import path

from buildersplant.views import (
    BuilderPlantListView,
    BuilderPlantListCreateView,
    BuilderPlantRetrieveUpdateDestroyView,
)

app_name = "buildersplant"

urlpatterns = [
    path("", BuilderPlantListView.as_view(), name="list"),
    path("create/", BuilderPlantListCreateView.as_view(), name="create"),
    path(
        "<str:reference>/",
        BuilderPlantRetrieveUpdateDestroyView.as_view(),
        name="retrieve_update_destroy",
    ),
]
