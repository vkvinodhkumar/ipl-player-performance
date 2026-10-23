# Day 10: Final Model Selection and Production-Candidate Training

## Execution status
```text
dataset                   target    status detail
batting          next_match_runs COMPLETED       
bowling       next_match_wickets COMPLETED       
bowling next_match_runs_conceded COMPLETED       
```

## Final candidate test metrics
```text
dataset                   target selected_model_from_day8  features  train_rows  validation_rows  final_fit_rows_train_plus_validation  test_rows test_start   test_end       MAE      RMSE       R2  mean_residual_actual_minus_predicted
batting          next_match_runs         LinearRegression        15       12621             2704                                 15325       2705 2024-04-13 2026-05-29 16.850733 22.619524 0.105080                              2.555942
bowling       next_match_wickets         LinearRegression        15        9886             2118                                 12004       2119 2024-04-08 2026-05-29  0.767798  0.989258 0.026481                              0.040727
bowling next_match_runs_conceded                  XGBoost        15        9886             2118                                 12004       2119 2024-04-08 2026-05-29  9.516070 12.015263 0.053118                              3.337681
```

## Model manifest
```text
dataset                   target       model_name                                                                                            model_path                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               feature_columns_json  training_rows_including_validation training_start_date training_end_date test_start_date test_end_date                      created_utc python_version pandas_version scikit_learn_version  random_state                                                                                     notes
batting          next_match_runs LinearRegression          D:\Git\Personal\ipl-player-performance\models\day10\batting_next_match_runs_candidate.joblib                   ["prior_career_batting_runs", "prior_last5_mean_batting_runs", "prior_last5_count_batting_runs", "prior_career_batting_balls_faced", "prior_last5_mean_batting_balls_faced", "prior_last5_count_batting_balls_faced", "prior_career_batting_fours", "prior_last5_mean_batting_fours", "prior_last5_count_batting_fours", "prior_career_batting_sixes", "prior_last5_mean_batting_sixes", "prior_last5_count_batting_sixes", "prior_career_batting_strike_rate", "prior_last5_mean_batting_strike_rate", "prior_last5_count_batting_strike_rate"]                               15325          2008-04-18        2024-04-13      2024-04-13    2026-05-29 2026-10-23T15:56:09.834439+00:00        3.12.14          3.0.6                1.9.1            42 Candidate trained on chronological train+validation; test used only for final diagnostic.
bowling       next_match_wickets LinearRegression       D:\Git\Personal\ipl-player-performance\models\day10\bowling_next_match_wickets_candidate.joblib ["prior_career_bowling_wickets", "prior_last5_mean_bowling_wickets", "prior_last5_count_bowling_wickets", "prior_career_bowling_runs_conceded", "prior_last5_mean_bowling_runs_conceded", "prior_last5_count_bowling_runs_conceded", "prior_career_bowling_legal_balls", "prior_last5_mean_bowling_legal_balls", "prior_last5_count_bowling_legal_balls", "prior_career_bowling_dots", "prior_last5_mean_bowling_dots", "prior_last5_count_bowling_dots", "prior_career_bowling_economy", "prior_last5_mean_bowling_economy", "prior_last5_count_bowling_economy"]                               12004          2008-04-18        2024-04-08      2024-04-08    2026-05-29 2026-10-23T15:56:09.918906+00:00        3.12.14          3.0.6                1.9.1            42 Candidate trained on chronological train+validation; test used only for final diagnostic.
bowling next_match_runs_conceded          XGBoost D:\Git\Personal\ipl-player-performance\models\day10\bowling_next_match_runs_conceded_candidate.joblib ["prior_career_bowling_wickets", "prior_last5_mean_bowling_wickets", "prior_last5_count_bowling_wickets", "prior_career_bowling_runs_conceded", "prior_last5_mean_bowling_runs_conceded", "prior_last5_count_bowling_runs_conceded", "prior_career_bowling_legal_balls", "prior_last5_mean_bowling_legal_balls", "prior_last5_count_bowling_legal_balls", "prior_career_bowling_dots", "prior_last5_mean_bowling_dots", "prior_last5_count_bowling_dots", "prior_career_bowling_economy", "prior_last5_mean_bowling_economy", "prior_last5_count_bowling_economy"]                               12004          2008-04-18        2024-04-08      2024-04-08    2026-05-29 2026-10-23T15:56:10.393751+00:00        3.12.14          3.0.6                1.9.1            42 Candidate trained on chronological train+validation; test used only for final diagnostic.
```

## Outputs
- `reports/day10/final_candidate_test_metrics.csv`
- `reports/day10/final_candidate_test_predictions.csv`
- `reports/day10/model_manifest.csv`
- `reports/day10/final_split_summary.csv`
- `reports/day10/task_status.csv`
- `models/day10/*_candidate.joblib`
- `docs/day10_final_model_selection.md`

## Method
- Model names are carried forward from Day 8 validation-based selection.
- Feature candidates are restricted to numeric `prior_...` columns.
- Chronological row split remains 70% training, 15% validation, 15% test.
- The selected model is refit on train + validation data.
- The held-out test partition is used only for final diagnostic metrics.
- Imputation remains inside the fitted scikit-learn pipeline.
- The manifest records feature columns, model path, dates, and library versions.
- No performance result is asserted until this notebook is executed successfully on the user's actual project data.

## Limitations
A row-based split can put records from the same match into different partitions. Candidate artifacts are not production-ready until feature generation, grouped/time-based validation, reproducibility, and API input validation are reviewed.

## Next
Day 11: establish a leakage-safe sequence dataset design for the LSTM/GRU experiments.
