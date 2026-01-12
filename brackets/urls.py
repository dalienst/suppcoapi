from django.urls import path

from brackets.views import (
    BracketListCreateView,
    BracketRetrieveUpdateDestroyView,
    BracketListView,
)

app_name = "brackets"

urlpatterns = [
    path("", BracketListView.as_view(), name="brackets-list"),
    path(
        "list-create/",
        BracketListCreateView.as_view(),
        name="brackets-list-create",
    ),
    path(
        "<str:reference>/",
        BracketRetrieveUpdateDestroyView.as_view(),
        name="brackets-retrieve-update-destroy",
    ),
]
