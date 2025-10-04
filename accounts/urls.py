from django.urls import path

from accounts.views import (
    LoginView,
    SupplierCreateView,
    ContractorCreateView,
    UserDetailView,
    VerifyAccountView,
    RequestPasswordResetView,
    PasswordResetView,
    UsersListView,
    UserPublicProfile,
    OwnerDetailView,
    EmployeeCreatedByOwnerView,
)

app_name = "accounts"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("<str:id>/", UserDetailView.as_view(), name="user-detail"),
    path("", UsersListView.as_view(), name="users-list"),
    path(
        "user/<str:username>/", UserPublicProfile.as_view(), name="user-public-profile"
    ),
    path("signup/supplier/", SupplierCreateView.as_view(), name="supplier-create"),
    path(
        "signup/contractor/", ContractorCreateView.as_view(), name="contractor-create"
    ),
    path(
        "verify-email/<str:uidb64>/<str:token>/",
        VerifyAccountView.as_view(),
        name="verify-email",
    ),
    # Password reset
    path("password/reset/", RequestPasswordResetView.as_view(), name="password-reset"),
    path("password/new/", PasswordResetView.as_view(), name="password-reset"),
    # Owners
    path("owner/<str:id>/", OwnerDetailView.as_view(), name="owner-detail"),
    path("add/employee/", EmployeeCreatedByOwnerView.as_view(), name="employee-create"),
]
