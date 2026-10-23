# Day 28 — Prediction Dashboard Report

Generated: 2026-10-23T21:50:06

## Created files
- `django_api\ipl_api\templates\ipl_api\dashboard_day28.html`
- `django_api\ipl_api\static\ipl_api\js\dashboard_day28.js`
- `django_api\ipl_api\static\ipl_api\css\dashboard_day28.css`
- `django_api\ipl_api\dashboard_views_day28.py`
- `django_api/ipl_api/urls.py` (route merged directly)

## Django check
Exit code: 0

Output:
System check identified no issues (0 silenced).

## Source-level endpoint indicators
- batting prediction: possible source match
- bowling prediction: possible source match
- generic prediction: possible source match
- batch prediction: possible source match
- model metrics endpoint: possible source match

## Model manifests
- `reports\day10\model_manifest.csv`: found
- `reports\day12\model_artifacts_manifest.csv`: found
- `reports\day23\model_manifest.csv`: not found
- `reports\day23\model_artifacts_manifest.csv`: not found

## Smoke test
Exit code: 0

Output:
/ => (400, 'text/plain; charset=utf-8', None)
/api/eda/summary/ => (400, 'text/plain; charset=utf-8', None)
/api/dashboard/ => (400, 'text/plain; charset=utf-8', None)
/api/dashboard-day28/ => (400, 'text/plain; charset=utf-8', None)

## URL repair
The notebook rebuilds the app URL configuration with actual newline characters and registers only routes whose view modules are present.

## Required verification
1. Confirm the notebook merged the Day 28 route into `django_api/ipl_api/urls.py` and preserved existing routes.
2. Restart Django and open `http://127.0.0.1:8000/api/dashboard-day28/`.
3. Use the exact request schema from the existing prediction API.
4. Test single prediction and batch prediction separately.
5. Read MAE, RMSE and R² from saved evaluation reports or a real metrics endpoint.

## Limitations
- Source keyword matches do not prove routes are registered.
- Successful page rendering does not prove model inference works.
- This notebook does not retrain models or fabricate evaluation metrics.
