from django.urls import path

from plumbing.views import (
    PlumbingListCreateView,
    PlumbingRetrieveUpdateDestroyView,
    PlumbingListView,
)

app_name = "plumbing"

urlpatterns = [
    path("create/", PlumbingListCreateView.as_view(), name="plumbing-list-create"),
    path(
        "<str:reference>/",
        PlumbingRetrieveUpdateDestroyView.as_view(),
        name="plumbing-retrieve-update-destroy",
    ),
    path("", PlumbingListView.as_view(), name="plumbing-list"),
]
