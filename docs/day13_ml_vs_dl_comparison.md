# Day 13 — ML vs Deep Learning Comparison

## Input availability
```text
         source                                                                                        path status                                                                                                                                                                                                      columns
   day8_metrics            D:\Git\Personal\ipl-player-performance\reports\day8\model_comparison_metrics.csv  FOUND                                                                                                          dataset, target, model, split, feature_count, train_rows, validation_rows, test_rows, MAE, RMSE, R2
 day8_selection          D:\Git\Personal\ipl-player-performance\reports\day8\validation_model_selection.csv  FOUND                                                                                                                                  dataset, target, selected_by_validation_mae, validation_mae, saved_pipeline
  day10_metrics       D:\Git\Personal\ipl-player-performance\reports\day10\final_candidate_test_metrics.csv  FOUND dataset, target, selected_model_from_day8, features, train_rows, validation_rows, final_fit_rows_train_plus_validation, test_rows, test_start, test_end, MAE, RMSE, R2, mean_residual_actual_minus_predicted
   day10_splits                D:\Git\Personal\ipl-player-performance\reports\day10\final_split_summary.csv  FOUND                                                     dataset, target, all_usable_rows, train_rows, validation_rows, test_rows, train_start, train_end, validation_start, validation_end, test_start, test_end
  day12_metrics     D:\Git\Personal\ipl-player-performance\reports\day12\selected_lstm_gru_test_metrics.csv  FOUND                              dataset, target, selected_architecture, train_samples, validation_samples, test_samples, feature_count, test_MAE, test_RMSE, test_R2, test_mean_residual_actual_minus_predicted
day12_selection D:\Git\Personal\ipl-player-performance\reports\day12\validation_architecture_comparison.csv  FOUND                                                                                                                    dataset, target, architecture, epochs_run, validation_MAE, validation_RMSE, validation_R2
   day12_splits        D:\Git\Personal\ipl-player-performance\reports\day12\chronological_split_summary.csv  FOUND                                                                                                                                             dataset, target, split, rows, target_date_start, target_date_end
```

## Final candidate metrics
```text
                  target  model_family            model       MAE      RMSE       R2                 source
         next_match_runs  Classical ML LinearRegression 16.850733 22.619524 0.105080 Day 10 final candidate
         next_match_runs Deep learning             LSTM 16.706738 22.493524 0.106153 Day 12 final candidate
      next_match_wickets  Classical ML LinearRegression  0.767798  0.989258 0.026481 Day 10 final candidate
      next_match_wickets Deep learning              GRU  0.790386  1.000189 0.018323 Day 12 final candidate
next_match_runs_conceded  Classical ML          XGBoost  9.516070 12.015263 0.053118 Day 10 final candidate
next_match_runs_conceded Deep learning              GRU  9.456311 11.845119 0.063147 Day 12 final candidate
```

## Test period review
```text
              source    status test_start   test_end
 Day 10 classical ML AVAILABLE 2024-04-08 2026-05-29
Day 12 deep learning AVAILABLE 2008-05-03 2026-05-31
```

## Interpretation
```text
                  target                                              interpretation
         next_match_runs No definitive winner — test-period comparability unresolved
      next_match_wickets No definitive winner — test-period comparability unresolved
next_match_runs_conceded No definitive winner — test-period comparability unresolved
```

**Comparability note:** Test date ranges differ. Treat scores as indicative, not a controlled head-to-head comparison.

## Outputs
- `reports/day13/ml_vs_dl_model_comparison.csv`
- `reports/day13/test_period_comparability.csv`
- `reports/day13/comparison_interpretation.csv`
- `reports/day13/input_status.csv`
- `docs/day13_ml_vs_dl_comparison.md`

## Method and limitations
- Day 10 is the selected classical ML candidate's final test metrics.
- Day 12 is the selected LSTM/GRU candidate's final test metrics.
- Day 8 provides baseline context; validation and test metrics are not interchangeable.
- Metrics: MAE, RMSE, and R².
- Lower MAE/RMSE and higher R² are generally preferable, but comparison requires compatible test populations.
- A row/sample-level chronological split may place different players from the same match across partition boundaries.
- No performance values or winners are hardcoded.

## Next
Day 14: robustness review, deep-learning error analysis, and candidate-model decision.
