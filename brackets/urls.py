from django.urls import path

from brackets.views import BracketListCreateView, BracketRetrieveUpdateDestroyView

app_name = "brackets"

urlpatterns = [
    path("", BracketListCreateView.as_view(), name="brackets-list-create"),
    path(
        "<str:reference>/",
        BracketRetrieveUpdateDestroyView.as_view(),
        name="brackets-retrieve-update-destroy",
    ),
]
