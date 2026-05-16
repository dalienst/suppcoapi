from django.urls import path

from companies.views import CompanyDetailView, CompanyListView, MyCompanyDetailView

app_name = "companies"

urlpatterns = [
    path("", CompanyListView.as_view(), name="company-list"),
    path("my/", MyCompanyDetailView.as_view(), name="my-company-detail"),
    path("<str:reference>/", CompanyDetailView.as_view(), name="company-detail"),
]
