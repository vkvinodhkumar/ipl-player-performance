
import csv
import json
from pathlib import Path

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

ROOT_DIR = Path(settings.BASE_DIR).parent
BAT_FEATURES = ROOT_DIR / "data" / "processed" / "batting_next_match_features.csv"
BOWL_FEATURES = ROOT_DIR / "data" / "processed" / "bowling_next_match_features.csv"
TARGETS = {
    "next_match_runs": (BAT_FEATURES, "player_name"),
    "next_match_wickets": (BOWL_FEATURES, "player_name"),
    "next_match_runs_conceded": (BOWL_FEATURES, "player_name"),
}

def _read_rows(path):
    if not path.is_file():
        raise FileNotFoundError(f"Feature dataset not found: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))

def _find_model_config(target):
    from .prediction_views import MODEL_CONFIGS
    return next((item for item in MODEL_CONFIGS if item.get("target") == target), None)

def _as_number(value):
    if value is None or value == "":
        return None
    try:
        number = float(value)
        if number != number or number in (float("inf"), float("-inf")):
            return None
        return number
    except (TypeError, ValueError):
        return None

@require_GET
def player_name_options_day28(request):
    query = request.GET.get("q", "").strip().casefold()
    if not query:
        return JsonResponse({"query": query, "results": []})
    path = BAT_FEATURES
    try:
        rows = _read_rows(path)
    except FileNotFoundError as exc:
        return JsonResponse({"detail": str(exc)}, status=503)
    names = sorted({r.get("player_name", "").strip() for r in rows
                    if query in r.get("player_name", "").strip().casefold()})
    return JsonResponse({"query": query, "results": names[:25]})

@require_POST
def player_name_prediction_day28(request):
    try:
        body = json.loads(request.body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"detail": "Request body must be valid JSON."}, status=400)
    if not isinstance(body, dict):
        return JsonResponse({"detail": "Request body must be a JSON object."}, status=400)
    player_name = str(body.get("player_name", "")).strip()
    target = str(body.get("target", "next_match_runs")).strip()
    if not player_name:
        return JsonResponse({"detail": "player_name is required."}, status=400)
    if target not in TARGETS:
        return JsonResponse({"detail": "Unsupported target.", "allowed_targets": list(TARGETS)}, status=400)
    path, name_column = TARGETS[target]
    try:
        rows = _read_rows(path)
    except FileNotFoundError as exc:
        return JsonResponse({"detail": str(exc)}, status=503)
    matches = [r for r in rows if r.get(name_column, "").strip().casefold() == player_name.casefold()]
    if not matches:
        matches = [r for r in rows if player_name.casefold() in r.get(name_column, "").strip().casefold()]
    if not matches:
        return JsonResponse({"detail": "Player not found in the relevant feature dataset.",
                             "player_name": player_name, "target": target}, status=404)
    # Use the latest available feature row; target/next-match columns are never passed as inputs.
    date_key = "match_date" if any(r.get("match_date") for r in matches) else "date"
    matches.sort(key=lambda r: (r.get(date_key, ""), r.get("match_id", "")))
    row = matches[-1]
    config = _find_model_config(target)
    if config is None:
        return JsonResponse({"detail": f"No saved model configuration for target {target}."}, status=503)
    feature_names = config.get("features", [])
    if not feature_names:
        return JsonResponse({"detail": "Model feature manifest is empty."}, status=503)
    payload = {}
    missing = []
    for feature in feature_names:
        # Never use the known future target or next-match identifiers as model features.
        if feature.startswith("next_match_") or feature in {"match_id", "date", "match_date", "player_name", "player_id"}:
            missing.append(feature)
            continue
        number = _as_number(row.get(feature))
        if number is None:
            missing.append(feature)
        else:
            payload[feature] = number
    if missing:
        return JsonResponse({"detail": "Latest player row cannot supply all required numeric model features.",
                             "missing_or_non_numeric_features": missing,
                             "player_name": row.get("player_name", player_name),
                             "target": target}, status=422)
    try:
        from .prediction_views import _predict
        value, error = _predict(config, payload)
        if error:
            return JsonResponse(error, status=400)
    except Exception as exc:
        return JsonResponse({"detail": "Model inference failed.", "error": str(exc)}, status=500)
    return JsonResponse({
        "player_name": row.get("player_name", player_name),
        "target": target,
        "prediction": value,
        "model": config.get("model_name", config.get("name", "configured model")),
        "feature_row_date": row.get(date_key),
        "features_used": payload,
        "note": "Estimate based on the latest available historical feature row; not a guarantee."
    })

@require_GET
def model_metrics_day28(request):
    # Return only metrics found in actual saved evaluation CSVs; never synthesize metrics.
    reports_root = ROOT_DIR / "reports"
    candidates = []
    for csv_path in reports_root.rglob("*.csv"):
        low = str(csv_path).casefold()
        if any(part in low for part in ("day10", "day12", "day13", "day14")) and "metric" in csv_path.name.casefold() or any(
            token in csv_path.name.casefold() for token in ("model_comparison", "test_metrics", "evaluation_metrics", "metric_summary")
        ):
            try:
                with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
                    reader = csv.DictReader(handle)
                    rows = list(reader)
                if rows and reader.fieldnames:
                    candidates.append({"file": str(csv_path.relative_to(ROOT_DIR)), "columns": reader.fieldnames, "rows": rows})
            except (OSError, csv.Error):
                continue
    if not candidates:
        return JsonResponse({"detail": "No saved evaluation CSV containing model metrics was found.",
                             "searched": "reports/day10, day12, day13 and day14"}, status=404)
    return JsonResponse({"source": "saved evaluation CSV files", "reports": candidates})
