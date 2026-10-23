import json
from pathlib import Path
import numpy as np
import pandas as pd
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

TARGETS = {"next_match_runs", "next_match_wickets", "next_match_runs_conceded"}

def _path_from_manifest(root, value):
    p = Path(str(value))
    if p.is_absolute() and p.exists():
        return p
    candidates = [root / p, root.parent / p]
    parts = list(p.parts)
    if "models" in parts:
        candidates.append(root.parent.joinpath(*parts[parts.index("models"):]))
        candidates.append(root.joinpath(*parts[parts.index("models"):]))
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]

@csrf_exempt
@require_POST
def deep_learning_prediction(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"detail": "Body must be valid JSON."}, status=400)
    target = payload.get("target")
    if target not in TARGETS:
        return JsonResponse({"detail": "Unsupported target.", "allowed_targets": sorted(TARGETS)}, status=400)
    try:
        sequence = np.asarray(payload.get("sequence"), dtype=np.float32)
    except (TypeError, ValueError):
        return JsonResponse({"detail": "sequence must contain numeric values."}, status=400)
    if sequence.ndim != 2 or sequence.shape[0] != 5 or sequence.shape[1] < 1:
        return JsonResponse({"detail": "sequence must be 5 x feature_count numeric rows."}, status=400)
    if not np.isfinite(sequence).all():
        return JsonResponse({"detail": "sequence contains NaN or infinite values."}, status=400)
    root = Path(settings.BASE_DIR).parent
    manifest_candidates = [
        root / "reports" / "day12" / "model_artifacts_manifest.csv",
        root / "reports" / "day12_model_artifacts_manifest.csv",
        root / "reports" / "day12" / "model_artifacts_manifest.csv",
    ]
    manifest_path = next((p for p in manifest_candidates if p.exists()), None)
    if manifest_path is None:
        return JsonResponse({"detail": "Day 12 model artifact manifest not found.", "searched": [str(p) for p in manifest_candidates]}, status=503)
    try:
        manifest = pd.read_csv(manifest_path)
        target_col = next((c for c in ["target", "target_name", "prediction_target"] if c in manifest.columns), None)
        if not target_col:
            return JsonResponse({"detail": "Manifest is missing a target column.", "columns": list(manifest.columns)}, status=503)
        row_df = manifest[manifest[target_col].astype(str).str.strip().eq(target)]
        if row_df.empty:
            return JsonResponse({"detail": "No saved DL model for this target.", "target": target}, status=503)
        row = row_df.iloc[0].to_dict()
        model_col = next((c for c in ["model_path", "model_file", "artifact_path"] if c in row and pd.notna(row[c])), None)
        if not model_col:
            return JsonResponse({"detail": "Manifest has no model_path field.", "columns": list(manifest.columns)}, status=503)
        model_path = _path_from_manifest(root, row[model_col])
        if not model_path.exists():
            return JsonResponse({"detail": "Saved model file not found.", "path": str(model_path)}, status=503)
        import tensorflow as tf
        model = tf.keras.models.load_model(model_path)
        feature_width = sequence.shape[1]
        imputer_col = next((c for c in ["imputer_path", "imputer_file"] if c in row and pd.notna(row[c])), None)
        scaler_col = next((c for c in ["scaler_path", "scaler_file"] if c in row and pd.notna(row[c])), None)
        # Saved preprocessing is applied if supplied in the artifact manifest.
        processed = sequence.astype(np.float32)
        import joblib
        if imputer_col:
            imputer_path = _path_from_manifest(root, row[imputer_col])
            if not imputer_path.exists():
                return JsonResponse({"detail": "Saved imputer not found.", "path": str(imputer_path)}, status=503)
            imputer = joblib.load(imputer_path)
            processed = imputer.transform(processed).astype(np.float32)
        if scaler_col:
            scaler_path = _path_from_manifest(root, row[scaler_col])
            if not scaler_path.exists():
                return JsonResponse({"detail": "Saved scaler not found.", "path": str(scaler_path)}, status=503)
            scaler = joblib.load(scaler_path)
            processed = scaler.transform(processed).astype(np.float32)
        expected = tuple(model.input_shape[1:])
        if len(expected) != 2 or expected[0] not in (None, 5) or expected[1] not in (None, processed.shape[1]):
            return JsonResponse({"detail": "Input shape mismatch.", "expected": list(model.input_shape), "received": list(processed.shape)}, status=400)
        pred = np.asarray(model.predict(processed[np.newaxis, :, :], verbose=0)).reshape(-1)
        if pred.size == 0 or not np.isfinite(float(pred[0])):
            return JsonResponse({"detail": "Model returned a non-finite prediction."}, status=503)
        return JsonResponse({"target": target, "prediction": float(pred[0]), "model_type": "DL",
                             "model_file": model_path.name, "sequence_length": 5,
                             "feature_count": int(processed.shape[1]),
                             "preprocessing": {"imputer_loaded": bool(imputer_col), "scaler_loaded": bool(scaler_col)}})
    except Exception as exc:
        return JsonResponse({"detail": "DL inference failed.", "error": str(exc)}, status=503)
