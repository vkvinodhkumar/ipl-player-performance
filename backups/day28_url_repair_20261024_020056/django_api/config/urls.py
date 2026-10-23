from ipl_api.dashboard_views_day26 import dashboard_day25
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path("api/dashboard/", dashboard_day25, name="ipl-dashboard-alias"),

    path("", RedirectView.as_view(url="/api/dashboard/", permanent=False), name="home"),
    path("api/", include("ipl_api.urls")),
    path("admin/", admin.site.urls),
]
