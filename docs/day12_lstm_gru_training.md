# Day 12 — LSTM/GRU Regression Training

## Task status
```text
dataset                   target    status detail
batting          next_match_runs COMPLETED       
bowling       next_match_wickets COMPLETED       
bowling next_match_runs_conceded COMPLETED       
```

## Validation architecture comparison
```text
dataset                   target architecture  epochs_run  validation_MAE  validation_RMSE  validation_R2
batting          next_match_runs         LSTM          38       16.325451        21.915191       0.104197
batting          next_match_runs          GRU          46       16.329929        21.831988       0.110986
bowling       next_match_wickets         LSTM          14        0.806983         1.037216       0.032260
bowling       next_match_wickets          GRU          17        0.804842         1.039777       0.027475
bowling next_match_runs_conceded         LSTM          54        8.450019        10.666042       0.136492
bowling next_match_runs_conceded          GRU          38        8.445145        10.655641       0.138176
```

## Selected architecture test metrics
```text
dataset                   target selected_architecture  train_samples  validation_samples  test_samples  feature_count  test_MAE  test_RMSE  test_R2  test_mean_residual_actual_minus_predicted
batting          next_match_runs                  LSTM          11074                2373          2374             15 16.706738  22.493524 0.106153                                   2.379298
bowling       next_match_wickets                   GRU           8634                1850          1851             15  0.790386   1.000189 0.018323                                  -0.007816
bowling next_match_runs_conceded                   GRU           8634                1850          1851             15  9.456311  11.845119 0.063147                                   3.307186
```

## Artifacts
```text
dataset                   target selected_architecture                                                                                     model_path                                                                                            imputer_path                                                                                            scaler_path                                                                                  feature_manifest_path
batting          next_match_runs                  LSTM         D:\Git\Personal\ipl-player-performance\models\day12\batting_next_match_runs_lstm.keras         D:\Git\Personal\ipl-player-performance\models\day12\batting_next_match_runs_lstm_imputer.joblib         D:\Git\Personal\ipl-player-performance\models\day12\batting_next_match_runs_lstm_scaler.joblib         D:\Git\Personal\ipl-player-performance\models\day12\batting_next_match_runs_lstm_features.json
bowling       next_match_wickets                   GRU       D:\Git\Personal\ipl-player-performance\models\day12\bowling_next_match_wickets_gru.keras       D:\Git\Personal\ipl-player-performance\models\day12\bowling_next_match_wickets_gru_imputer.joblib       D:\Git\Personal\ipl-player-performance\models\day12\bowling_next_match_wickets_gru_scaler.joblib       D:\Git\Personal\ipl-player-performance\models\day12\bowling_next_match_wickets_gru_features.json
bowling next_match_runs_conceded                   GRU D:\Git\Personal\ipl-player-performance\models\day12\bowling_next_match_runs_conceded_gru.keras D:\Git\Personal\ipl-player-performance\models\day12\bowling_next_match_runs_conceded_gru_imputer.joblib D:\Git\Personal\ipl-player-performance\models\day12\bowling_next_match_runs_conceded_gru_scaler.joblib D:\Git\Personal\ipl-player-performance\models\day12\bowling_next_match_runs_conceded_gru_features.json
```

## Method
- Sequence length: 5 historical matches.
- Architectures: LSTM and GRU, one scalar regression output per target.
- Targets: `next_match_runs`, `next_match_wickets`, `next_match_runs_conceded`.
- Split: chronological sample-level 70% train / 15% validation / 15% test by target match date.
- Preprocessing: median imputation and standard scaling fitted on flattened training sequences only.
- Training: Adam optimizer, MSE loss, MAE metric, early stopping on validation loss, `shuffle=False`.
- Selection: lowest validation MAE, validation RMSE as tie-breaker.
- Test partition: evaluated after architecture selection; not used to choose the architecture.
- Seed: 42.
- TensorFlow available at run time: True.

## Limitations
- Sequence split is sample-level; samples from different players in the same match may cross split boundaries.
- This experiment uses a small fixed architecture and is a baseline, not a claim of optimal deep-learning performance.
- Validate all feature definitions for leakage and review the actual task status before accepting the metrics.

## Outputs
- `reports/day12/selected_lstm_gru_test_metrics.csv`
- `reports/day12/selected_lstm_gru_test_predictions.csv`
- `reports/day12/training_history.csv`
- `reports/day12/validation_architecture_comparison.csv`
- `reports/day12/chronological_split_summary.csv`
- `reports/day12/model_artifacts_manifest.csv`
- `reports/day12/task_status.csv`
- `models/day12/`
- `docs/day12_lstm_gru_training.md`

## Next
Day 13: error analysis and comparison of the deep-learning models against the Day 8 tree-based baselines.
