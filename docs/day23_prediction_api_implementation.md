# Day 23 — Prediction API Implementation

- Generated: 2026-10-22T00:09:36
- ML manifest entries: 3
- DL manifest entries: 3
- Django check return code: 0
- Day 21 regression return code: 0

## Model mapping

- `next_match_runs` → `models/day10/batting_next_match_runs_candidate.joblib` (LinearRegression); features: 15.
- `next_match_wickets` → `models/day10/bowling_next_match_wickets_candidate.joblib` (LinearRegression); features: 15.
- `next_match_runs_conceded` → `models/day10/bowling_next_match_runs_conceded_candidate.joblib` (XGBoost); features: 15.

## Generated files

- `django_api/ipl_api/prediction_views.py`
- `django_api/ipl_api/day23_prediction_urls_patch.txt`
- `reports/day10/artifact_path_validation_day23.csv`

## Limitations

The generated endpoints use the Day 10 ML candidate artifacts and exact ordered feature lists in model_manifest.csv. They accept numeric model features directly; they do not derive feature values from player_name or database history. Deep-learning inference is not enabled in this module; it requires sequence-window construction matching the Day 11/12 feature manifests.

The URL patch must be merged manually and the endpoints must be smoke-tested after registration. Do not treat the API as verified until valid and invalid payload tests pass.
