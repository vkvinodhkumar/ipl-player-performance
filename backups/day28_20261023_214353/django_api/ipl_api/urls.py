from django.urls import path
from .eda_summary_day26 import eda_summary_day26
from .dashboard_views_day26 import dashboard_day25
from .views import PlayerListAPIView, PlayerDetailAPIView

urlpatterns = [
    path("eda/summary/", eda_summary_day26, name="eda-summary-day26"),
    path("dashboard/", dashboard_day25, name="ipl-dashboard"),
    path("players/", PlayerListAPIView.as_view(), name="player-list"),
    path("players/<str:player_name>/", PlayerDetailAPIView.as_view(), name="player-detail"),
]
