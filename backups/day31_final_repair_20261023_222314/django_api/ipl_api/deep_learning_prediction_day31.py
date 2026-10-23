import json
from pathlib import Path
import numpy as np
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_POST
def deep_learning_prediction(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"detail": "Body must be valid JSON."}, status=400)
    target = payload.get("target")
    if target not in {"next_match_runs", "next_match_wickets", "next_match_runs_conceded"}:
        return JsonResponse({"detail": "Unsupported target."}, status=400)
    try:
        arr = np.asarray(payload.get("sequence"), dtype=np.float32)
    except (TypeError, ValueError):
        return JsonResponse({"detail": "sequence must be numeric."}, status=400)
    if arr.ndim != 2 or arr.shape[0] != 5 or arr.shape[1] < 1 or not np.isfinite(arr).all():
        return JsonResponse({"detail": "sequence must be a finite numeric 5 x feature_count array."}, status=400)
    if payload.get("preprocessed") is not True:
        return JsonResponse({"detail": "Apply the saved Day 12 imputer/scaler before submitting; raw inputs are rejected."}, status=400)
    root = Path(settings.BASE_DIR).parent
    manifests = [root / "reports" / "day12" / "model_artifacts_manifest.csv",
                 root / "reports" / "day12_model_artifacts_manifest.csv"]
    manifest = next((p for p in manifests if p.exists()), None)
    if manifest is None:
        return JsonResponse({"detail": "Day 12 model_artifacts_manifest.csv not found."}, status=503)
    try:
        import pandas as pd
        df = pd.read_csv(manifest)
        tc = next((c for c in ["target", "target_name", "prediction_target"] if c in df.columns), None)
        mc = next((c for c in ["model_path", "model_file", "artifact_path"] if c in df.columns), None)
        if not tc or not mc:
            return JsonResponse({"detail": "Manifest requires target and model_path columns."}, status=503)
        found = df[df[tc].astype(str).eq(target)]
        if found.empty:
            return JsonResponse({"detail": "No saved DL model registered for target."}, status=503)
        model_path = Path(str(found.iloc[0][mc]))
        if not model_path.is_absolute():
            model_path = root / model_path
        if not model_path.exists():
            parts = list(model_path.parts)
            if "models" in parts:
                model_path = root.joinpath(*parts[parts.index("models"):])
        if not model_path.exists():
            return JsonResponse({"detail": "Saved model file not found.", "path": str(model_path)}, status=503)
        import tensorflow as tf
        model = tf.keras.models.load_model(model_path)
        expected = tuple(model.input_shape[1:])
        if len(expected) != 2 or expected[0] not in (None, 5) or expected[1] not in (None, arr.shape[1]):
            return JsonResponse({"detail": "Input shape does not match saved model.", "expected": list(model.input_shape), "received": list(arr.shape)}, status=400)
        pred = np.asarray(model.predict(arr[np.newaxis, :, :], verbose=0)).reshape(-1)
        return JsonResponse({"target": target, "prediction": float(pred[0]), "model_type": "DL"})
    except Exception as exc:
        return JsonResponse({"detail": "DL inference failed.", "error": str(exc)}, status=503)
