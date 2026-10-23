# Day 14 — Deep Learning Robustness Review

## Input availability
```text
              source status                                                                                        path  rows
       day12_metrics  FOUND     D:\Git\Personal\ipl-player-performance\reports\day12\selected_lstm_gru_test_metrics.csv     3
   day12_predictions  FOUND D:\Git\Personal\ipl-player-performance\reports\day12\selected_lstm_gru_test_predictions.csv  6076
      day12_manifest  FOUND           D:\Git\Personal\ipl-player-performance\reports\day12\model_artifacts_manifest.csv     3
        day12_status  FOUND                        D:\Git\Personal\ipl-player-performance\reports\day12\task_status.csv     3
    day13_comparison  FOUND          D:\Git\Personal\ipl-player-performance\reports\day13\ml_vs_dl_model_comparison.csv     6
day13_interpretation  FOUND          D:\Git\Personal\ipl-player-performance\reports\day13\comparison_interpretation.csv     3
```

## Error summary
```text
                  target  rows  MAE_recomputed  RMSE_recomputed  mean_residual_actual_minus_predicted  median_absolute_error  p90_absolute_error  p95_absolute_error  max_absolute_error
         next_match_runs  2374       16.706737        22.493525                              2.379298              13.352062           34.245324           45.780291          119.059250
next_match_runs_conceded  1851        9.456312        11.845119                              3.307186               7.983307           19.361038           23.433829           46.539734
      next_match_wickets  1851        0.790386         1.000189                             -0.007816               0.850177            1.325027            1.942337            4.040541
```

## Metric consistency
```text
                  target status  recomputed_MAE  reported_MAE  recomputed_RMSE  reported_RMSE
         next_match_runs  MATCH       16.706737     16.706738        22.493525      22.493524
next_match_runs_conceded  MATCH        9.456312      9.456311        11.845119      11.845119
      next_match_wickets  MATCH        0.790386      0.790386         1.000189       1.000189
```

## Artifact validation
```text
                  target status                      detail
         next_match_runs   PASS All listed artifacts exist.
      next_match_wickets   PASS All listed artifacts exist.
next_match_runs_conceded   PASS All listed artifacts exist.
```

## Candidate readiness
```text
                  target             readiness                                                      notes
         next_match_runs READY FOR INTEGRATION Required reports and artifacts passed the notebook checks.
      next_match_wickets READY FOR INTEGRATION Required reports and artifacts passed the notebook checks.
next_match_runs_conceded READY FOR INTEGRATION Required reports and artifacts passed the notebook checks.
```

## Outputs
- `reports/day14/deep_learning_error_summary.csv`
- `reports/day14/largest_deep_learning_errors.csv`
- `reports/day14/grouped_error_summary.csv`
- `reports/day14/metric_consistency_check.csv`
- `reports/day14/artifact_validation.csv`
- `reports/day14/candidate_readiness.csv`
- `reports/day14/input_status.csv`
- `docs/day14_deep_learning_robustness_review.md`

## Method and limitations
- Residual = actual minus predicted.
- Positive mean residual indicates average under-prediction; negative indicates average over-prediction.
- Recomputed metrics are compared to Day 12 reported metrics for consistency only.
- Test errors are diagnostics, not a basis for choosing a different architecture.
- Artifact presence is not proof of production readiness or scientific validity.
- Row/sample-level chronological splits may place different players from the same match across partitions.
- No error rows are removed automatically.

## Next
Day 15: configure MySQL integration and prepare the project database schema.
