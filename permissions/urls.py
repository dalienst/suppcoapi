from django.urls import path

from permissions.views import PermissionListCreateView, PermissionDetailView

app_name = "permissions"

urlpatterns = [
    path("", PermissionListCreateView.as_view(), name="permission-list-create"),
    path("<str:reference>", PermissionDetailView.as_view(), name="permission-detail"),
]
