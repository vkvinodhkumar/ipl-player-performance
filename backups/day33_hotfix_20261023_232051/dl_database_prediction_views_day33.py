import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from django.conf import settings
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

SUPPORTED_TARGETS = {"next_match_runs", "next_match_wickets", "next_match_runs_conceded"}
TABLE_BY_TARGET = {
    "next_match_runs": "stg_ipl_batting_player_match",
    "next_match_wickets": "stg_ipl_bowling_player_match",
    "next_match_runs_conceded": "stg_ipl_bowling_player_match",
}

def _root():
    base = Path(settings.BASE_DIR).resolve()
    return base.parent if base.name == "django_api" else base

def _resolve(value, root, base=None):
    p = Path(str(value))
    candidates = [p] if p.is_absolute() else [root / p, root / "models" / p]
    if base and not p.is_absolute():
        candidates.append(Path(base) / p)
    parts = list(p.parts)
    if "models" in parts:
        candidates.append(root.joinpath(*parts[parts.index("models"):]))
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    raise FileNotFoundError(f"Artifact not found: {value}")

def _manifest_row(target):
    root = _root()
    candidates = [
        root / "reports/day12/model_artifacts_manifest.csv",
        root / "reports/day12/model_manifest.csv",
        root / "reports/day23/model_artifacts_manifest.csv",
    ]
    manifest_path = next((p for p in candidates if p.exists()), None)
    if not manifest_path:
        raise FileNotFoundError("Day 12 model artifact manifest is missing.")
    frame = pd.read_csv(manifest_path)
    target_col = next((c for c in ["target", "target_name"] if c in frame.columns), None)
    if not target_col:
        raise ValueError("Manifest has no target/target_name column.")
    rows = frame[frame[target_col].astype(str).eq(target)]
    if rows.empty:
        raise ValueError(f"No saved DL artifact row for {target}.")
    row = rows.iloc[0].to_dict()
    return row, manifest_path

def _features(row, root, manifest_path):
    value = next((row.get(c) for c in ["feature_manifest_path", "features_path", "feature_path"] if row.get(c) and str(row.get(c)) != "nan"), None)
    if not value:
        raise ValueError("Manifest row has no feature_manifest_path.")
    path = _resolve(value, root, manifest_path.parent)
    info = json.loads(path.read_text(encoding="utf-8"))
    features = info.get("feature_columns_in_order", info.get("feature_columns", info.get("features", [])))
    if not isinstance(features, list) or not features:
        raise ValueError(f"No ordered feature list in {path.name}.")
    return [str(x) for x in features], path

def _artifact(row, key, root, manifest_path):
    value = row.get(key)
    if value is None or str(value).strip() in {"", "nan", "None"}:
        return None
    return _resolve(value, root, manifest_path.parent)

def _last_five(player_name, table, feature_names):
    allowed = {"stg_ipl_batting_player_match", "stg_ipl_bowling_player_match"}
    if table not in allowed:
        raise ValueError("Invalid table configuration.")
    with connection.cursor() as cur:
        cur.execute(f"SHOW COLUMNS FROM `{table}`")
        columns = [r[0] for r in cur.fetchall()]
    lower = {c.lower(): c for c in columns}
    player_col = next((lower[c] for c in ["player_name", "player_name_norm", "batter", "bowler", "player"] if c in lower), None)
    date_col = next((lower[c] for c in ["match_date", "date"] if c in lower), None)
    match_col = next((lower[c] for c in ["match_id", "id"] if c in lower), None)
    if not player_col:
        raise ValueError(f"{table} has no recognized player-name column.")
    if not date_col and not match_col:
        raise ValueError(f"{table} has no reliable match ordering column.")
    order = []
    if date_col: order.append(f"`{date_col}` ASC")
    if match_col: order.append(f"`{match_col}` ASC")
    select_cols = ", ".join(f"`{c}`" for c in columns)
    sql = f"SELECT {select_cols} FROM `{table}` WHERE LOWER(`{player_col}`) = LOWER(%s) ORDER BY {', '.join(order)}"
    with connection.cursor() as cur:
        cur.execute(sql, [player_name.strip()])
        rows = cur.fetchall()
    if len(rows) < 5:
        raise ValueError(f"Found only {len(rows)} historical rows for {player_name}; five are required.")
    records = [dict(zip(columns, row)) for row in rows]

    # Build the same past-only engineered features expected by the Day 12 manifests.
    # Raw staging rows are used; no current/future match outcome is used as a feature.
    metric_aliases = {
        "batting_runs": ["runs", "batter_runs", "batsman_runs"],
        "batting_balls_faced": ["balls_faced", "balls"],
        "batting_fours": ["fours", "four"],
        "batting_sixes": ["sixes", "six"],
        "batting_strike_rate": ["strike_rate"],
        "bowling_wickets": ["wickets", "player_dismissals"],
        "bowling_runs_conceded": ["runs_conceded", "bowler_runs_conceded"],
        "bowling_legal_balls": ["legal_balls", "balls_bowled"],
        "bowling_dots": ["dots", "dot_balls"],
        "bowling_economy": ["economy"],
    }
    def raw_value(record, aliases):
        record_lower = {str(k).lower(): v for k, v in record.items()}
        for alias in aliases:
            value = record_lower.get(alias)
            if value is not None:
                try:
                    value = float(value)
                    if np.isfinite(value):
                        return value
                except (TypeError, ValueError):
                    pass
        return None

    history = []
    enriched = []
    for record in records:
        item = dict(record)
        for feature in feature_names:
            m = re.match(r"prior_(career|last5_mean|last5_count)_(batting|bowling)_(.+)$", feature)
            if not m:
                continue
            kind, role, metric = m.groups()
            key = f"{role}_{metric}"
            aliases = metric_aliases.get(key, [metric])
            prior_values = [v for v in (raw_value(prev, aliases) for prev in history) if v is not None]
            if kind == "career":
                item[feature] = float(sum(prior_values)) if prior_values else 0.0
            elif kind == "last5_mean":
                item[feature] = float(np.mean(prior_values[-5:])) if prior_values else 0.0
            else:
                item[feature] = float(min(len(prior_values), 5))
        enriched.append(item)
        history.append(record)

    # Keep the final five enriched chronological match rows for the sequence model.
    return enriched[-5:], list(dict.fromkeys(columns + feature_names))

@csrf_exempt
@require_POST
def predict_dl_from_database(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
        player_name = str(payload.get("player_name", "")).strip()
        target = str(payload.get("target", "")).strip()
        if not player_name:
            return JsonResponse({"detail": "player_name is required."}, status=400)
        if target not in SUPPORTED_TARGETS:
            return JsonResponse({"detail": "Unsupported target.", "supported_targets": sorted(SUPPORTED_TARGETS)}, status=400)
        table = TABLE_BY_TARGET[target]
        manifest_row, manifest_path = _manifest_row(target)
        feature_names, feature_path = _features(manifest_row, _root(), manifest_path)
        records, db_columns = _last_five(player_name, table, feature_names)
        missing = [name for name in feature_names if name not in db_columns]
        if missing:
            return JsonResponse({
                "detail": "Database rows do not contain all features required by the saved DL model.",
                "missing_features": missing,
                "feature_manifest": str(feature_path),
                "table": table,
            }, status=422)
        matrix = np.asarray([[float(record[name]) if record[name] is not None else np.nan for name in feature_names] for record in records], dtype=float)
        model_path = _artifact(manifest_row, "model_path", _root(), manifest_path)
        if not model_path:
            raise FileNotFoundError("Model path is missing from the Day 12 manifest.")
        model = None
        try:
            from tensorflow.keras.models import load_model
            model = load_model(model_path, compile=False)
        except Exception as keras_error:
            try:
                model = joblib.load(model_path)
            except Exception:
                raise RuntimeError(f"Could not load saved DL model: {keras_error}")
        imputer_path = _artifact(manifest_row, "imputer_path", _root(), manifest_path)
        scaler_path = _artifact(manifest_row, "scaler_path", _root(), manifest_path)
        if np.isnan(matrix).any():
            if not imputer_path:
                return JsonResponse({"detail": "Sequence has null features and no saved imputer is configured."}, status=422)
            matrix = joblib.load(imputer_path).transform(matrix)
        if scaler_path:
            matrix = joblib.load(scaler_path).transform(matrix)
        expected = getattr(model, "input_shape", None)
        if expected and len(expected) == 3:
            if matrix.shape[1] != expected[2]:
                return JsonResponse({"detail": "Feature count does not match model input.", "actual_features": int(matrix.shape[1]), "expected_features": int(expected[2])}, status=422)
            x = matrix.reshape(1, matrix.shape[0], matrix.shape[1])
        else:
            x = matrix.reshape(1, matrix.shape[0], matrix.shape[1])
        pred = np.asarray(model.predict(x, verbose=0)).reshape(-1)
        if pred.size == 0 or not np.isfinite(float(pred[0])):
            raise ValueError("Model returned an empty or non-finite prediction.")
        return JsonResponse({
            "player_name": player_name,
            "target": target,
            "prediction": float(pred[0]),
            "model_file": model_path.name,
            "history_rows_used": len(records),
            "sequence_order": "oldest_to_newest",
            "feature_order": feature_names,
            "matches_used": [{k: (str(v) if v is not None else None) for k, v in r.items() if k in {"match_id", "match_date", "date", "season", "team", "opposition", "runs", "wickets", "runs_conceded"}} for r in records],
        })
    except (ValueError, FileNotFoundError, KeyError) as exc:
        return JsonResponse({"detail": str(exc)}, status=422)
    except Exception as exc:
        return JsonResponse({"detail": f"DL inference failed: {type(exc).__name__}: {exc}"}, status=500)
