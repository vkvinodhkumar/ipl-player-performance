# Day 7: Leakage-Safe Baseline Modelling

## Data readiness audit
```text
dataset  rows  players  missing_player  missing_match_id  invalid_current_date  invalid_target_date  duplicate_match_player_keys
batting 18030      633               0                 0                     0                    0                            0
bowling 14123      503               0                 0                     0                    0                            0
```

## Target summary
```text
dataset                   target  non_null  missing      mean  median       std  min   max
batting          next_match_runs     18030        0 20.704049    13.0 21.830644  0.0 175.0
bowling       next_match_wickets     14123        0  0.922396     1.0  1.001237  0.0   6.0
bowling next_match_runs_conceded     14123        0 26.897260    26.0 11.188855  0.0  76.0
```

## Feature eligibility counts
```text
decision  ELIGIBLE_CANDIDATE  EXCLUDE  REVIEW_MANUALLY
dataset                                               
batting                   15       23               11
bowling                   15       25               10
```

## Chronological split boundaries
```text
dataset                   target  total_rows  train_rows  validation_rows  test_rows train_start  train_end validation_start validation_end test_start   test_end                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    feature_columns
batting          next_match_runs       18030       12621             2704       2705  2008-04-18 2021-10-08       2021-10-08     2024-04-13 2024-04-13 2026-05-29                   prior_career_batting_runs, prior_last5_mean_batting_runs, prior_last5_count_batting_runs, prior_career_batting_balls_faced, prior_last5_mean_batting_balls_faced, prior_last5_count_batting_balls_faced, prior_career_batting_fours, prior_last5_mean_batting_fours, prior_last5_count_batting_fours, prior_career_batting_sixes, prior_last5_mean_batting_sixes, prior_last5_count_batting_sixes, prior_career_batting_strike_rate, prior_last5_mean_batting_strike_rate, prior_last5_count_batting_strike_rate
bowling       next_match_wickets       14123        9886             2118       2119  2008-04-18 2021-10-01       2021-10-01     2024-04-08 2024-04-08 2026-05-29 prior_career_bowling_wickets, prior_last5_mean_bowling_wickets, prior_last5_count_bowling_wickets, prior_career_bowling_runs_conceded, prior_last5_mean_bowling_runs_conceded, prior_last5_count_bowling_runs_conceded, prior_career_bowling_legal_balls, prior_last5_mean_bowling_legal_balls, prior_last5_count_bowling_legal_balls, prior_career_bowling_dots, prior_last5_mean_bowling_dots, prior_last5_count_bowling_dots, prior_career_bowling_economy, prior_last5_mean_bowling_economy, prior_last5_count_bowling_economy
bowling next_match_runs_conceded       14123        9886             2118       2119  2008-04-18 2021-10-01       2021-10-01     2024-04-08 2024-04-08 2026-05-29 prior_career_bowling_wickets, prior_last5_mean_bowling_wickets, prior_last5_count_bowling_wickets, prior_career_bowling_runs_conceded, prior_last5_mean_bowling_runs_conceded, prior_last5_count_bowling_runs_conceded, prior_career_bowling_legal_balls, prior_last5_mean_bowling_legal_balls, prior_last5_count_bowling_legal_balls, prior_career_bowling_dots, prior_last5_mean_bowling_dots, prior_last5_count_bowling_dots, prior_career_bowling_economy, prior_last5_mean_bowling_economy, prior_last5_count_bowling_economy
```

## Baseline metrics
```text
dataset                   target            model      split  rows  feature_count       MAE      RMSE        R2
batting          next_match_runs      DummyMedian validation  2704             15 16.475222 23.850519 -0.129310
batting          next_match_runs      DummyMedian       test  2705             15 17.912754 26.069777 -0.188754
batting          next_match_runs LinearRegression validation  2704             15 15.864845 21.231884  0.105058
batting          next_match_runs LinearRegression       test  2705             15 16.835979 22.663426  0.101603
bowling       next_match_wickets      DummyMedian validation  2118             15  0.789424  1.051551 -0.000545
bowling       next_match_wickets      DummyMedian       test  2119             15  0.759320  1.002828 -0.000410
bowling       next_match_wickets LinearRegression validation  2118             15  0.789086  1.036961  0.027026
bowling       next_match_wickets LinearRegression       test  2119             15  0.767192  0.990279  0.024471
bowling next_match_runs_conceded      DummyMedian validation  2118             15  9.516997 11.945718 -0.089322
bowling next_match_runs_conceded      DummyMedian       test  2119             15 10.924021 13.644409 -0.221064
bowling next_match_runs_conceded LinearRegression validation  2118             15  8.502858 10.748316  0.118114
bowling next_match_runs_conceded LinearRegression       test  2119             15  9.650816 12.116601  0.037079
```

## Outputs
- `reports/day7/data_readiness_audit.csv`
- `reports/day7/target_summary.csv`
- `reports/day7/feature_eligibility_review.csv`
- `reports/day7/chronological_split_summary.csv`
- `reports/day7/baseline_model_metrics.csv`

## Safeguards and limitations
- Current-match outcomes, targets, identifiers, and future-match metadata are excluded from automatic predictors.
- Automatic predictor candidates are numeric `prior_...` columns; inspect their construction in the Day 4 notebook.
- Chronological split is row-based (70%/15%/15%), so records from one match may cross a split boundary.
- Same-day ordering uses match ID as a tie-breaker where start times are unavailable.
- Imputation is fitted within each model pipeline on training data only.
- No metric is asserted until this notebook is run against the user's actual data.

## Next step
Day 8: train Random Forest and XGBoost regressors and compare them with these baselines.
