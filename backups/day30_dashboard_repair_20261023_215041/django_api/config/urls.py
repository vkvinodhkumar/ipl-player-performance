from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path(
        "",
        RedirectView.as_view(url="/api/dashboard/", permanent=False),
        name="home",
    ),
    path("api/", include("ipl_api.urls")),
    path("admin/", admin.site.urls),
]
