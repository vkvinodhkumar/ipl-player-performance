from django.urls import path
from .views import PlayerListAPIView, PlayerDetailAPIView
from .dashboard_views_day28 import dashboard_day28
from .eda_summary_day26 import eda_summary_day26
from .eda_views import EDABattingAPIView, EDABowlingAPIView, EDASeasonAPIView, EDAVenueAPIView, EDAOppositionAPIView, EDARecentFormAPIView
from .prediction_views import BattingPredictionAPIView, BowlingPredictionAPIView, UnifiedPredictionAPIView
from .batch_prediction_views import BatchPredictionAPIView
from .player_name_prediction_views_day28 import player_name_prediction_day28, player_name_options_day28, model_metrics_day28

from .dashboard_views_day26 import dashboard_day25\nfrom .dl_database_prediction_views_day33 import predict_dl_from_database
urlpatterns = [\n    path("dashboard/", dashboard_day25, name="ipl-dashboard"),
    path("dashboard-day28/", dashboard_day28, name="ipl-dashboard-day28"),
    path("players/", PlayerListAPIView.as_view(), name="player-list"),
    path("players/<str:player_name>/", PlayerDetailAPIView.as_view(), name="player-detail"),
    path("eda/summary/", eda_summary_day26, name="eda-summary-day26"),
    path("eda/batting/", EDABattingAPIView.as_view(), name="eda-batting"),
    path("eda/bowling/", EDABowlingAPIView.as_view(), name="eda-bowling"),
    path("eda/season/", EDASeasonAPIView.as_view(), name="eda-season"),
    path("eda/venue/", EDAVenueAPIView.as_view(), name="eda-venue"),
    path("eda/opposition/", EDAOppositionAPIView.as_view(), name="eda-opposition"),
    path("eda/recent-form/", EDARecentFormAPIView.as_view(), name="eda-recent-form"),
    path("predict/", UnifiedPredictionAPIView.as_view(), name="predict-unified"),
    path("predict/batting/", BattingPredictionAPIView.as_view(), name="predict-batting"),
    path("predict/bowling/", BowlingPredictionAPIView.as_view(), name="predict-bowling"),
    path("predict/batch/", BatchPredictionAPIView.as_view(), name="predict-batch"),
    path("players/search-options/", player_name_options_day28, name="player-name-options-day28"),
    path("predict/player/", player_name_prediction_day28, name="predict-player-name-day28"),
    path("eda/model-metrics/", model_metrics_day28, name="model-metrics-day28"),
    path("predict/dl/database/", predict_dl_from_database, name="predict-dl-database"),
]
