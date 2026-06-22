from django.urls import path

from branches.views import BranchListCreateView, BranchDetailView

app_name = "branches"

urlpatterns = [
    path("", BranchListCreateView.as_view(), name="branch-list"),
    path("<str:reference>/", BranchDetailView.as_view(), name="branch-detail"),
]
