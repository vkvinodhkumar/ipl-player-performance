import json
from pathlib import Path
import joblib
import numpy as np
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

MODEL_CONFIGS = [{'dataset': 'batting', 'target': 'next_match_runs', 'model_name': 'LinearRegression', 'model_relative_path': 'models/day10/batting_next_match_runs_candidate.joblib', 'features': ['prior_career_batting_runs', 'prior_last5_mean_batting_runs', 'prior_last5_count_batting_runs', 'prior_career_batting_balls_faced', 'prior_last5_mean_batting_balls_faced', 'prior_last5_count_batting_balls_faced', 'prior_career_batting_fours', 'prior_last5_mean_batting_fours', 'prior_last5_count_batting_fours', 'prior_career_batting_sixes', 'prior_last5_mean_batting_sixes', 'prior_last5_count_batting_sixes', 'prior_career_batting_strike_rate', 'prior_last5_mean_batting_strike_rate', 'prior_last5_count_batting_strike_rate']}, {'dataset': 'bowling', 'target': 'next_match_wickets', 'model_name': 'LinearRegression', 'model_relative_path': 'models/day10/bowling_next_match_wickets_candidate.joblib', 'features': ['prior_career_bowling_wickets', 'prior_last5_mean_bowling_wickets', 'prior_last5_count_bowling_wickets', 'prior_career_bowling_runs_conceded', 'prior_last5_mean_bowling_runs_conceded', 'prior_last5_count_bowling_runs_conceded', 'prior_career_bowling_legal_balls', 'prior_last5_mean_bowling_legal_balls', 'prior_last5_count_bowling_legal_balls', 'prior_career_bowling_dots', 'prior_last5_mean_bowling_dots', 'prior_last5_count_bowling_dots', 'prior_career_bowling_economy', 'prior_last5_mean_bowling_economy', 'prior_last5_count_bowling_economy']}, {'dataset': 'bowling', 'target': 'next_match_runs_conceded', 'model_name': 'XGBoost', 'model_relative_path': 'models/day10/bowling_next_match_runs_conceded_candidate.joblib', 'features': ['prior_career_bowling_wickets', 'prior_last5_mean_bowling_wickets', 'prior_last5_count_bowling_wickets', 'prior_career_bowling_runs_conceded', 'prior_last5_mean_bowling_runs_conceded', 'prior_last5_count_bowling_runs_conceded', 'prior_career_bowling_legal_balls', 'prior_last5_mean_bowling_legal_balls', 'prior_last5_count_bowling_legal_balls', 'prior_career_bowling_dots', 'prior_last5_mean_bowling_dots', 'prior_last5_count_bowling_dots', 'prior_career_bowling_economy', 'prior_last5_mean_bowling_economy', 'prior_last5_count_bowling_economy']}]
_CACHE = {}

def _model_path(config):
    return Path(settings.BASE_DIR).parent / config["model_relative_path"]

def _get_model(config):
    target = config["target"]
    if target not in _CACHE:
        path = _model_path(config)
        if not path.is_file():
            raise FileNotFoundError(f"Model artifact not found for target {target}: {path}")
        _CACHE[target] = joblib.load(path)
    return _CACHE[target]

def _validate_payload(payload, config):
    if not isinstance(payload, dict):
        return None, {"detail": "Request body must be a JSON object."}
    missing = [name for name in config["features"] if name not in payload]
    if missing:
        return None, {"detail": "Missing required model features.", "missing_features": missing}
    bad = []
    values = []
    for name in config["features"]:
        value = payload[name]
        if isinstance(value, bool):
            bad.append(name)
            continue
        try:
            number = float(value)
            if not np.isfinite(number):
                raise ValueError()
            values.append(number)
        except (TypeError, ValueError):
            bad.append(name)
    if bad:
        return None, {"detail": "All model features must be finite numeric values.", "invalid_features": bad}
    return np.asarray([values], dtype=float), None

def _predict(config, payload):
    matrix, error = _validate_payload(payload, config)
    if error:
        return None, error
    model = _get_model(config)
    prediction = model.predict(matrix)
    value = float(np.asarray(prediction).reshape(-1)[0])
    if not np.isfinite(value):
        raise ValueError("Model returned a non-finite prediction.")
    return value, None

class BattingPredictionAPIView(APIView):
    def post(self, request):
        config = next((c for c in MODEL_CONFIGS if c["target"] == "next_match_runs"), None)
        if config is None:
            return Response({"detail": "Batting model is not configured."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        try:
            value, error = _predict(config, request.data)
            if error:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            return Response({"target": config["target"], "model": config["model_name"], "prediction": value})
        except FileNotFoundError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception:
            return Response({"detail": "Prediction failed. Check server logs for the underlying error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BowlingPredictionAPIView(APIView):
    def post(self, request):
        configs = [c for c in MODEL_CONFIGS if c["target"] in {"next_match_wickets", "next_match_runs_conceded"}]
        if len(configs) != 2:
            return Response({"detail": "Both bowling models must be configured."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        results = {}
        try:
            for config in configs:
                value, error = _predict(config, request.data)
                if error:
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)
                results[config["target"]] = {"model": config["model_name"], "prediction": value}
            return Response({"predictions": results})
        except FileNotFoundError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception:
            return Response({"detail": "Prediction failed. Check server logs for the underlying error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UnifiedPredictionAPIView(APIView):
    def post(self, request):
        target = request.data.get("target")
        config = next((c for c in MODEL_CONFIGS if c["target"] == target), None)
        if config is None:
            return Response({"detail": "Unsupported target.", "supported_targets": [c["target"] for c in MODEL_CONFIGS]},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            value, error = _predict(config, request.data.get("features", request.data))
            if error:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            return Response({"target": target, "model": config["model_name"], "prediction": value})
        except FileNotFoundError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception:
            return Response({"detail": "Prediction failed. Check server logs for the underlying error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
