from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .prediction_views import MODEL_CONFIGS, _predict

class BatchPredictionAPIView(APIView):
    MAX_BATCH_SIZE = 500

    def post(self, request):
        target = request.data.get("target")
        records = request.data.get("records")
        config = next((c for c in MODEL_CONFIGS if c["target"] == target), None)
        if config is None:
            return Response(
                {"detail": "Unsupported target.", "supported_targets": [c["target"] for c in MODEL_CONFIGS]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not isinstance(records, list) or not records:
            return Response({"detail": "'records' must be a non-empty list."}, status=status.HTTP_400_BAD_REQUEST)
        if len(records) > self.MAX_BATCH_SIZE:
            return Response({"detail": f"Batch exceeds maximum of {self.MAX_BATCH_SIZE} records."},
                            status=status.HTTP_400_BAD_REQUEST)
        results = []
        for index, record in enumerate(records):
            try:
                value, error = _predict(config, record)
                if error:
                    return Response({"record_index": index, "error": error}, status=status.HTTP_400_BAD_REQUEST)
                results.append({"record_index": index, "target": target, "prediction": value})
            except FileNotFoundError as exc:
                return Response({"detail": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            except Exception:
                return Response({"detail": "Batch prediction failed. Check server logs for the underlying error."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"target": target, "count": len(results), "predictions": results})
