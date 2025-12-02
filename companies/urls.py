from django.urls import path

from companies.views import CompanyDetailView, CompanyListView, MyCompanyListView

app_name = "companies"

urlpatterns = [
    path("", CompanyListView.as_view(), name="company-list"),
    path("my/", MyCompanyListView.as_view(), name="my-company-list"),
    path("<str:identity>/", CompanyDetailView.as_view(), name="company-detail"),
]
