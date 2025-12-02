from django.urls import path

from employment.views import (
    EmployeeAssignView,
    EmployeeUnassignView,
    EmploymentListView,
)

app_name = "employment"

urlpatterns = [
    path("", EmploymentListView.as_view(), name="employment-list"),
    path("assign/", EmployeeAssignView.as_view(), name="employee-assign"),
    path(
        "unassign/",
        EmployeeUnassignView.as_view(),
        name="employee-unassign",
    ),
]
