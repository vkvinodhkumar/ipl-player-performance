# File documentation: `django_api\ipl_api\urls.py`

- Generated: 2026-10-24T02:01:30
- Exists at documentation time: True
- Bytes: 2143
- Purpose: Generated project asset.

## Key elements

## File content
```css
from django.urls import path
from .views import PlayerListAPIView, PlayerDetailAPIView
from .dashboard_views_day26 import dashboard_day25
from .eda_summary_day26 import eda_summary_day26
from .eda_views import EDABattingAPIView, EDABowlingAPIView, EDASeasonAPIView, EDAVenueAPIView, EDAOppositionAPIView, EDARecentFormAPIView
from .prediction_views import BattingPredictionAPIView, BowlingPredictionAPIView, UnifiedPredictionAPIView
from .batch_prediction_views import BatchPredictionAPIView
from .prediction_center_views_day28 import prediction_center_day28
from .player_name_prediction_views_day28 import player_name_prediction_day28, player_name_options_day28, model_metrics_day28

urlpatterns = [
    path("dashboard/", dashboard_day25, name="ipl-dashboard"),
    path("predictions/", prediction_center_day28, name="ipl-predictions"),
    path("players/", PlayerListAPIView.as_view(), name="player-list"),
    path("players/search-options/", player_name_options_day28, name="player-name-options-day28"),
    path("players/<str:player_name>/", PlayerDetailAPIView.as_view(), name="player-detail"),
    path("eda/summary/", eda_summary_day26, name="eda-summary"),
    path("eda/batting/", EDABattingAPIView.as_view(), name="eda-batting"),
    path("eda/bowling/", EDABowlingAPIView.as_view(), name="eda-bowling"),
    path("eda/season/", EDASeasonAPIView.as_view(), name="eda-season"),
    path("eda/venue/", EDAVenueAPIView.as_view(), name="eda-venue"),
    path("eda/opposition/", EDAOppositionAPIView.as_view(), name="eda-opposition"),
    path("eda/recent-form/", EDARecentFormAPIView.as_view(), name="eda-recent-form"),
    path("eda/model-metrics/", model_metrics_day28, name="model-metrics"),
    path("predict/", UnifiedPredictionAPIView.as_view(), name="predict-unified"),
    path("predict/batting/", BattingPredictionAPIView.as_view(), name="predict-batting"),
    path("predict/bowling/", BowlingPredictionAPIView.as_view(), name="predict-bowling"),
    path("predict/batch/", BatchPredictionAPIView.as_view(), name="predict-batch"),
    path("predict/player/", player_name_prediction_day28, name="predict-player-name-day28"),
]

```
