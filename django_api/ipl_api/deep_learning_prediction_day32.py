import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

TARGETS = {"next_match_runs", "next_match_wickets", "next_match_runs_conceded"}

def repo_root():
    base = Path(settings.BASE_DIR).resolve()
    return base.parent if base.name == "django_api" else base

def resolve_artifact(root, value, base_dir=None):
    p = Path(str(value))
    candidates = [p] if p.is_absolute() else [root/p, root/"models"/p]
    if base_dir and not p.is_absolute():
        candidates.append(Path(base_dir)/p)
    parts = list(p.parts)
    if "models" in parts:
        candidates.append(root.joinpath(*parts[parts.index("models"):]))
    for c in candidates:
        if c.exists():
            return c.resolve()
    return candidates[0].resolve()

def value_from(row, names):
    for name in names:
        value = row.get(name)
        if value is not None and not pd.isna(value) and str(value).strip():
            return str(value).strip()
    return None

def find_manifest(root):
    candidates = [root/"reports"/"day12"/"model_artifacts_manifest.csv",
                  root/"reports"/"day12_model_artifacts_manifest.csv"]
    if (root/"reports").exists():
        candidates += list((root/"reports").rglob("*model*artifact*manifest*.csv"))
    path = next((p for p in candidates if p.is_file()), None)
    if path is None:
        raise FileNotFoundError("Day 12 model_artifacts_manifest.csv not found under reports/.")
    return pd.read_csv(path), path

@csrf_exempt
@require_POST
def deep_learning_prediction(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"detail": "Request body must be valid JSON."}, status=400)
    target = str(payload.get("target", "")).strip()
    if target not in TARGETS:
        return JsonResponse({"detail": "Unsupported target.", "allowed_targets": sorted(TARGETS)}, status=400)
    if payload.get("preprocessed") is True:
        return JsonResponse({"detail": "Send raw values in Day 11 feature order. The endpoint applies saved Day 12 preprocessing; remove preprocessed:true."}, status=400)
    try:
        sequence = np.asarray(payload.get("sequence"), dtype=np.float32)
    except (TypeError, ValueError):
        return JsonResponse({"detail": "sequence must contain numeric values."}, status=400)
    if sequence.ndim != 2 or sequence.shape[0] != 5:
        return JsonResponse({"detail": "sequence must be exactly 5 chronological rows.", "received_shape": list(sequence.shape)}, status=400)
    if not np.isfinite(sequence).all():
        return JsonResponse({"detail": "sequence contains NaN or infinite values."}, status=400)

    root = repo_root()
    try:
        manifest, manifest_path = find_manifest(root)
    except Exception as exc:
        return JsonResponse({"detail": str(exc)}, status=503)
    target_col = next((c for c in ["target", "target_name", "prediction_target"] if c in manifest.columns), None)
    if not target_col:
        return JsonResponse({"detail": "Manifest is missing a target column.", "columns": list(manifest.columns)}, status=503)
    rows = manifest[manifest[target_col].astype(str).str.strip().eq(target)]
    if rows.empty:
        return JsonResponse({"detail": "No saved DL model is recorded for this target.", "target": target}, status=503)
    row = rows.iloc[0].to_dict()
    model_value = value_from(row, ["model_path", "model_file", "artifact_path"])
    feature_value = value_from(row, ["feature_manifest_path", "features_path", "feature_path"])
    if not model_value or not feature_value:
        return JsonResponse({"detail": "Manifest row must include model_path and feature_manifest_path.", "columns": list(manifest.columns)}, status=503)
    model_path = resolve_artifact(root, model_value, manifest_path.parent)
    feature_path = resolve_artifact(root, feature_value, manifest_path.parent)
    if not model_path.is_file():
        return JsonResponse({"detail": "Saved DL model not found.", "path": str(model_path)}, status=503)
    if not feature_path.is_file():
        return JsonResponse({"detail": "Day 11 feature manifest not found.", "path": str(feature_path)}, status=503)
    try:
        feature_info = json.loads(feature_path.read_text(encoding="utf-8"))
        features = feature_info.get("feature_columns_in_order", feature_info.get("feature_columns"))
        if not isinstance(features, list) or not features:
            raise ValueError("feature_columns_in_order missing or empty")
    except Exception as exc:
        return JsonResponse({"detail": "Cannot read ordered feature manifest.", "path": str(feature_path), "error": str(exc)}, status=503)
    if sequence.shape[1] != len(features):
        return JsonResponse({"detail": "Feature count mismatch.", "expected_feature_count": len(features),
                             "received_feature_count": int(sequence.shape[1]), "feature_names_in_order": features,
                             "hint": "Provide five rows with one number per feature in this exact order."}, status=400)

    imputer_value = value_from(row, ["imputer_path", "imputer_file"])
    scaler_value = value_from(row, ["scaler_path", "scaler_file"])
    try:
        flat = sequence.reshape(5, len(features))
        if imputer_value:
            path = resolve_artifact(root, imputer_value, manifest_path.parent)
            if not path.is_file():
                return JsonResponse({"detail": "Saved imputer not found.", "path": str(path)}, status=503)
            flat = joblib.load(path).transform(flat)
        if scaler_value:
            path = resolve_artifact(root, scaler_value, manifest_path.parent)
            if not path.is_file():
                return JsonResponse({"detail": "Saved scaler not found.", "path": str(path)}, status=503)
            flat = joblib.load(path).transform(flat)
        x = np.asarray(flat, dtype=np.float32).reshape(1, 5, len(features))
        import tensorflow as tf
        model = tf.keras.models.load_model(model_path)
        expected = tuple(model.input_shape[1:])
        if len(expected) != 2 or expected[0] not in (None, 5) or expected[1] not in (None, len(features)):
            return JsonResponse({"detail": "Model input shape does not match feature manifest.",
                                 "model_input_shape": list(model.input_shape), "feature_count": len(features)}, status=503)
        prediction = float(np.asarray(model.predict(x, verbose=0)).reshape(-1)[0])
    except Exception as exc:
        return JsonResponse({"detail": "DL inference failed while loading or applying saved artifacts.",
                             "error": str(exc), "model_path": str(model_path)}, status=503)
    return JsonResponse({"target": target, "prediction": prediction,
                         "model": value_from(row, ["architecture", "model_type", "selected_architecture"]) or "Saved LSTM/GRU",
                         "sequence_length": 5, "feature_count": len(features), "feature_names_in_order": features,
                         "preprocessing": {"imputer_applied": bool(imputer_value), "scaler_applied": bool(scaler_value)}})
