from django.urls import path

from roles.views import RoleListCreateView, RoleDetailView

app_name = "roles"

urlpatterns = [
    path("", RoleListCreateView.as_view(), name="role-list"),
    path("<str:identity>/", RoleDetailView.as_view(), name="role-detail"),
]
