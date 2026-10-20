# Day 9: Error Analysis, Feature Importance, and Model Review

## Status
Notebook execution status is represented by the task status report below. No metrics are hard-coded into this document.

## Task status
```text
dataset                   target    status                                             reason
batting          next_match_runs COMPLETED Selected by Day 8 validation MAE: LinearRegression
bowling       next_match_wickets COMPLETED Selected by Day 8 validation MAE: LinearRegression
bowling next_match_runs_conceded COMPLETED          Selected by Day 8 validation MAE: XGBoost
```

## Split summary
```text
dataset                   target   selected_model  rows  train_rows  validation_rows  test_rows train_start  train_end validation_start validation_end test_start   test_end  feature_count
batting          next_match_runs LinearRegression 18030       12621             2704       2705  2008-04-18 2021-10-08       2021-10-08     2024-04-13 2024-04-13 2026-05-29             15
bowling       next_match_wickets LinearRegression 14123        9886             2118       2119  2008-04-18 2021-10-01       2021-10-01     2024-04-08 2024-04-08 2026-05-29             15
bowling next_match_runs_conceded          XGBoost 14123        9886             2118       2119  2008-04-18 2021-10-01       2021-10-01     2024-04-08 2024-04-08 2026-05-29             15
```

## Error summary
```text
dataset                   target                 split  rows       MAE      RMSE        R2  mean_residual_actual_minus_predicted  median_absolute_error  p90_absolute_error  max_absolute_error
batting          next_match_runs test_final_diagnostic  2705 16.835979 22.663426  0.101603                              2.821742              13.220589           34.663988          121.722479
batting          next_match_runs            validation  2704 15.864845 21.231884  0.105058                              1.268018              12.366859           31.896621          114.401996
bowling next_match_runs_conceded test_final_diagnostic  2119  9.767157 12.360691 -0.002108                              4.187010               8.150419           19.876905           49.359316
bowling next_match_runs_conceded            validation  2118  8.490233 10.764133  0.115517                              1.870741               7.039113           17.559795           45.047338
bowling       next_match_wickets test_final_diagnostic  2119  0.767192  0.990279  0.024471                              0.054471               0.886932            1.283623            4.186592
bowling       next_match_wickets            validation  2118  0.789086  1.036961  0.027026                              0.047310               0.884755            1.289294            4.255998
```

## Top validation permutation importance
```text
dataset                   target   selected_model                                 feature  permutation_importance_mae_increase  importance_std evaluation_split
batting          next_match_runs LinearRegression        prior_career_batting_balls_faced                             1.605897        0.074373       validation
batting          next_match_runs LinearRegression           prior_last5_mean_batting_runs                             0.817615        0.058521       validation
batting          next_match_runs LinearRegression   prior_last5_count_batting_strike_rate                             0.763914        0.065864       validation
bowling next_match_runs_conceded          XGBoost      prior_career_bowling_runs_conceded                             0.265011        0.028953       validation
batting          next_match_runs LinearRegression              prior_career_batting_sixes                             0.233450        0.029606       validation
bowling next_match_runs_conceded          XGBoost               prior_career_bowling_dots                             0.198854        0.027451       validation
batting          next_match_runs LinearRegression               prior_career_batting_runs                             0.189351        0.045004       validation
bowling       next_match_wickets LinearRegression       prior_last5_count_bowling_economy                             0.155290        0.007139       validation
bowling next_match_runs_conceded          XGBoost  prior_last5_mean_bowling_runs_conceded                             0.133489        0.015187       validation
batting          next_match_runs LinearRegression              prior_career_batting_fours                             0.106334        0.014778       validation
bowling next_match_runs_conceded          XGBoost        prior_career_bowling_legal_balls                             0.056146        0.020705       validation
bowling next_match_runs_conceded          XGBoost           prior_last5_mean_bowling_dots                             0.052059        0.020819       validation
bowling next_match_runs_conceded          XGBoost    prior_last5_mean_bowling_legal_balls                             0.051355        0.014378       validation
batting          next_match_runs LinearRegression          prior_last5_mean_batting_fours                             0.048013        0.010873       validation
bowling next_match_runs_conceded          XGBoost        prior_last5_mean_bowling_economy                             0.041851        0.015778       validation
bowling next_match_runs_conceded          XGBoost            prior_career_bowling_wickets                             0.040306        0.023675       validation
bowling next_match_runs_conceded          XGBoost            prior_career_bowling_economy                             0.029559        0.018825       validation
batting          next_match_runs LinearRegression        prior_career_batting_strike_rate                             0.026844        0.009481       validation
bowling       next_match_wickets LinearRegression      prior_career_bowling_runs_conceded                             0.024943        0.004183       validation
bowling next_match_runs_conceded          XGBoost       prior_last5_count_bowling_wickets                             0.024668        0.006263       validation
bowling       next_match_wickets LinearRegression    prior_last5_mean_bowling_legal_balls                             0.023799        0.003738       validation
bowling       next_match_wickets LinearRegression prior_last5_count_bowling_runs_conceded                             0.016574        0.001742       validation
bowling       next_match_wickets LinearRegression          prior_last5_count_bowling_dots                             0.016574        0.001742       validation
bowling       next_match_wickets LinearRegression   prior_last5_count_bowling_legal_balls                             0.016574        0.001742       validation
bowling       next_match_wickets LinearRegression       prior_last5_count_bowling_wickets                             0.016574        0.001742       validation
bowling       next_match_wickets LinearRegression               prior_career_bowling_dots                             0.007740        0.001947       validation
batting          next_match_runs LinearRegression    prior_last5_mean_batting_strike_rate                             0.007157        0.023348       validation
bowling       next_match_wickets LinearRegression  prior_last5_mean_bowling_runs_conceded                             0.006980        0.001495       validation
bowling       next_match_wickets LinearRegression        prior_career_bowling_legal_balls                             0.006549        0.002104       validation
batting          next_match_runs LinearRegression   prior_last5_count_batting_balls_faced                            -0.014565        0.013113       validation
```

## Files produced
- `reports/day9/error_predictions.csv`
- `reports/day9/error_summary.csv`
- `reports/day9/largest_validation_errors.csv`
- `reports/day9/permutation_feature_importance.csv`
- `reports/day9/native_tree_feature_importance.csv`
- `reports/day9/split_summary.csv`
- `reports/day9/task_status.csv`
- `docs/day9_error_analysis_feature_importance.md`

## Methodology
- The Day 8 validation-selected model is reused for each target.
- Model is refit on the training partition only; validation supports diagnostics and permutation importance.
- Test partition metrics are a final diagnostic only and must not drive selection.
- Numeric `prior_...` columns are the only automatic predictor candidates.
- Metrics: MAE, RMSE, R², residual bias, median/p90/max absolute error.
- Feature importance is descriptive, model-dependent, and not causal.

## Limitations and decisions
- The chronological split is row-based (70/15/15); records from one match can cross boundaries.
- Permutation importance can be noisy for correlated features or small validation samples.
- A high-error row must be investigated against the source, target alignment, and player-match chronology before data is changed.
- No model should be promoted to production based on a single diagnostic notebook.

## Next starting point
Day 10: consolidate model evaluation and define the final training/evaluation protocol, including a safer match-date/group-aware split if the data supports it. Do not start Day 10 until Day 9 outputs and documentation are reviewed.
