from django.urls import path

from sites.views import SiteListCreateView, SiteDetailView

app_name = "sites"

urlpatterns = [
    path("", SiteListCreateView.as_view(), name="site-list"),
    path("<str:identity>/", SiteDetailView.as_view(), name="site-detail"),
]
