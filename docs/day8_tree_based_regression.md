# Day 8: Random Forest and XGBoost Regression

## Feature review
```text
                                 column          dtype           decision                                                        reason  missing_pct dataset
                               match_id          int64            EXCLUDE identifier, target, future metadata, or current-match outcome         0.00 batting
                                 season            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 batting
                                  venue            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 batting
                                   city            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         4.08 batting
                                 team_1            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 batting
                                 team_2            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 batting
                             match_type        float64  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature       100.00 batting
                                   team            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 batting
                             opposition            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 batting
                            player_name            str            EXCLUDE identifier, target, future metadata, or current-match outcome         0.00 batting
                              player_id            str            EXCLUDE identifier, target, future metadata, or current-match outcome         0.00 batting
                       player_name_norm            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 batting
                              team_norm            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 batting
                        opposition_norm            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 batting
                                   runs          int64            EXCLUDE identifier, target, future metadata, or current-match outcome         0.00 batting
                            balls_faced          int64            EXCLUDE identifier, target, future metadata, or current-match outcome         0.00 batting
                                  fours          int64            EXCLUDE identifier, target, future metadata, or current-match outcome         0.00 batting
                                  sixes          int64            EXCLUDE identifier, target, future metadata, or current-match outcome         0.00 batting
                       batting_position          int64            EXCLUDE identifier, target, future metadata, or current-match outcome         0.00 batting
                          was_dismissed           bool  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 batting
                         dismissal_kind            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature        21.86 batting
                          innings_count          int64  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 batting
                            strike_rate        float64            EXCLUDE identifier, target, future metadata, or current-match outcome         0.04 batting
                             match_date            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 batting
                            season_meta            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 batting
                             venue_meta            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 batting
                              city_meta            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         4.08 batting
                            team_1_meta            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 batting
                            team_2_meta            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 batting
                                   date datetime64[us]            EXCLUDE identifier, target, future metadata, or current-match outcome         0.00 batting
                        next_match_runs        float64            EXCLUDE identifier, target, future metadata, or current-match outcome         0.00 batting
                          next_match_id        float64            EXCLUDE identifier, target, future metadata, or current-match outcome         0.00 batting
                        next_match_date datetime64[us]            EXCLUDE identifier, target, future metadata, or current-match outcome         0.00 batting
                    matches_seen_before          int64  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 batting
              prior_career_batting_runs        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         3.51 batting
          prior_last5_mean_batting_runs        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         3.51 batting
         prior_last5_count_batting_runs        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         0.00 batting
       prior_career_batting_balls_faced        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         3.51 batting
   prior_last5_mean_batting_balls_faced        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         3.51 batting
  prior_last5_count_batting_balls_faced        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         0.00 batting
             prior_career_batting_fours        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         3.51 batting
         prior_last5_mean_batting_fours        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         3.51 batting
        prior_last5_count_batting_fours        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         0.00 batting
             prior_career_batting_sixes        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         3.51 batting
         prior_last5_mean_batting_sixes        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         3.51 batting
        prior_last5_count_batting_sixes        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         0.00 batting
       prior_career_batting_strike_rate        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         3.51 batting
   prior_last5_mean_batting_strike_rate        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         3.51 batting
  prior_last5_count_batting_strike_rate        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         0.00 batting
                               match_id          int64            EXCLUDE identifier, target, future metadata, or current-match outcome         0.00 bowling
                                 season            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 bowling
                                  venue            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 bowling
                                   city            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         4.17 bowling
                                 team_1            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 bowling
                                 team_2            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 bowling
                             match_type        float64  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature       100.00 bowling
                                   team            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 bowling
                             opposition            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 bowling
                            player_name            str            EXCLUDE identifier, target, future metadata, or current-match outcome         0.00 bowling
                              player_id            str            EXCLUDE identifier, target, future metadata, or current-match outcome         0.00 bowling
                       player_name_norm            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 bowling
                              team_norm            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 bowling
                        opposition_norm            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 bowling
                            legal_balls          int64            EXCLUDE identifier, target, future metadata, or current-match outcome         0.00 bowling
                          runs_conceded          int64            EXCLUDE identifier, target, future metadata, or current-match outcome         0.00 bowling
                                wickets          int64            EXCLUDE identifier, target, future metadata, or current-match outcome         0.00 bowling
                                  wides          int64            EXCLUDE identifier, target, future metadata, or current-match outcome         0.00 bowling
                                noballs          int64            EXCLUDE identifier, target, future metadata, or current-match outcome         0.00 bowling
                                   dots          int64            EXCLUDE identifier, target, future metadata, or current-match outcome         0.00 bowling
                          innings_count          int64  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 bowling
                                  overs        float64            EXCLUDE identifier, target, future metadata, or current-match outcome         0.00 bowling
                                economy        float64            EXCLUDE identifier, target, future metadata, or current-match outcome         0.01 bowling
                             match_date            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 bowling
                            season_meta            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 bowling
                             venue_meta            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 bowling
                              city_meta            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         4.17 bowling
                            team_1_meta            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 bowling
                            team_2_meta            str  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 bowling
                                   date datetime64[us]            EXCLUDE identifier, target, future metadata, or current-match outcome         0.00 bowling
                     next_match_wickets        float64            EXCLUDE identifier, target, future metadata, or current-match outcome         0.00 bowling
               next_match_runs_conceded        float64            EXCLUDE identifier, target, future metadata, or current-match outcome         0.00 bowling
                          next_match_id        float64            EXCLUDE identifier, target, future metadata, or current-match outcome         0.00 bowling
                        next_match_date datetime64[us]            EXCLUDE identifier, target, future metadata, or current-match outcome         0.00 bowling
                    matches_seen_before          int64  REVIEW_OR_EXCLUDE                 not an approved numeric prior-history feature         0.00 bowling
           prior_career_bowling_wickets        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         3.56 bowling
       prior_last5_mean_bowling_wickets        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         3.56 bowling
      prior_last5_count_bowling_wickets        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         0.00 bowling
     prior_career_bowling_runs_conceded        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         3.56 bowling
 prior_last5_mean_bowling_runs_conceded        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         3.56 bowling
prior_last5_count_bowling_runs_conceded        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         0.00 bowling
       prior_career_bowling_legal_balls        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         3.56 bowling
   prior_last5_mean_bowling_legal_balls        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         3.56 bowling
  prior_last5_count_bowling_legal_balls        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         0.00 bowling
              prior_career_bowling_dots        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         3.56 bowling
          prior_last5_mean_bowling_dots        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         3.56 bowling
         prior_last5_count_bowling_dots        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         0.00 bowling
           prior_career_bowling_economy        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         3.56 bowling
       prior_last5_mean_bowling_economy        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         3.56 bowling
      prior_last5_count_bowling_economy        float64 ELIGIBLE_CANDIDATE     numeric prior-history feature; verify source construction         0.00 bowling
```

## Chronological split summary
```text
dataset                   target  rows  train_rows  validation_rows  test_rows train_start  train_end validation_start validation_end test_start   test_end                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           features
batting          next_match_runs 18030       12621             2704       2705  2008-04-18 2021-10-08       2021-10-08     2024-04-13 2024-04-13 2026-05-29                   prior_career_batting_runs, prior_last5_mean_batting_runs, prior_last5_count_batting_runs, prior_career_batting_balls_faced, prior_last5_mean_batting_balls_faced, prior_last5_count_batting_balls_faced, prior_career_batting_fours, prior_last5_mean_batting_fours, prior_last5_count_batting_fours, prior_career_batting_sixes, prior_last5_mean_batting_sixes, prior_last5_count_batting_sixes, prior_career_batting_strike_rate, prior_last5_mean_batting_strike_rate, prior_last5_count_batting_strike_rate
bowling       next_match_wickets 14123        9886             2118       2119  2008-04-18 2021-10-01       2021-10-01     2024-04-08 2024-04-08 2026-05-29 prior_career_bowling_wickets, prior_last5_mean_bowling_wickets, prior_last5_count_bowling_wickets, prior_career_bowling_runs_conceded, prior_last5_mean_bowling_runs_conceded, prior_last5_count_bowling_runs_conceded, prior_career_bowling_legal_balls, prior_last5_mean_bowling_legal_balls, prior_last5_count_bowling_legal_balls, prior_career_bowling_dots, prior_last5_mean_bowling_dots, prior_last5_count_bowling_dots, prior_career_bowling_economy, prior_last5_mean_bowling_economy, prior_last5_count_bowling_economy
bowling next_match_runs_conceded 14123        9886             2118       2119  2008-04-18 2021-10-01       2021-10-01     2024-04-08 2024-04-08 2026-05-29 prior_career_bowling_wickets, prior_last5_mean_bowling_wickets, prior_last5_count_bowling_wickets, prior_career_bowling_runs_conceded, prior_last5_mean_bowling_runs_conceded, prior_last5_count_bowling_runs_conceded, prior_career_bowling_legal_balls, prior_last5_mean_bowling_legal_balls, prior_last5_count_bowling_legal_balls, prior_career_bowling_dots, prior_last5_mean_bowling_dots, prior_last5_count_bowling_dots, prior_career_bowling_economy, prior_last5_mean_bowling_economy, prior_last5_count_bowling_economy
```

## Model comparison metrics
```text
dataset                   target            model      split  feature_count  train_rows  validation_rows  test_rows       MAE      RMSE        R2
batting          next_match_runs      DummyMedian validation             15       12621             2704       2705 16.475222 23.850519 -0.129310
batting          next_match_runs      DummyMedian       test             15       12621             2704       2705 17.912754 26.069777 -0.188754
batting          next_match_runs LinearRegression validation             15       12621             2704       2705 15.864845 21.231884  0.105058
batting          next_match_runs LinearRegression       test             15       12621             2704       2705 16.835979 22.663426  0.101603
batting          next_match_runs     RandomForest validation             15       12621             2704       2705 16.176661 21.458592  0.085844
batting          next_match_runs     RandomForest       test             15       12621             2704       2705 17.008145 22.884593  0.083983
batting          next_match_runs          XGBoost validation             15       12621             2704       2705 15.931191 21.312452  0.098254
batting          next_match_runs          XGBoost       test             15       12621             2704       2705 16.918188 22.788992  0.091620
bowling       next_match_wickets      DummyMedian validation             15        9886             2118       2119  0.789424  1.051551 -0.000545
bowling       next_match_wickets      DummyMedian       test             15        9886             2118       2119  0.759320  1.002828 -0.000410
bowling       next_match_wickets LinearRegression validation             15        9886             2118       2119  0.789086  1.036961  0.027026
bowling       next_match_wickets LinearRegression       test             15        9886             2118       2119  0.767192  0.990279  0.024471
bowling       next_match_wickets     RandomForest validation             15        9886             2118       2119  0.822477  1.054177 -0.005548
bowling       next_match_wickets     RandomForest       test             15        9886             2118       2119  0.790675  1.000926  0.003382
bowling       next_match_wickets          XGBoost validation             15        9886             2118       2119  0.803011  1.044739  0.012377
bowling       next_match_wickets          XGBoost       test             15        9886             2118       2119  0.785701  1.001161  0.002912
bowling next_match_runs_conceded      DummyMedian validation             15        9886             2118       2119  9.516997 11.945718 -0.089322
bowling next_match_runs_conceded      DummyMedian       test             15        9886             2118       2119 10.924021 13.644409 -0.221064
bowling next_match_runs_conceded LinearRegression validation             15        9886             2118       2119  8.502858 10.748316  0.118114
bowling next_match_runs_conceded LinearRegression       test             15        9886             2118       2119  9.650816 12.116601  0.037079
bowling next_match_runs_conceded     RandomForest validation             15        9886             2118       2119  8.571248 10.853586  0.100755
bowling next_match_runs_conceded     RandomForest       test             15        9886             2118       2119  9.897280 12.503676 -0.025426
bowling next_match_runs_conceded          XGBoost validation             15        9886             2118       2119  8.490233 10.764133  0.115517
bowling next_match_runs_conceded          XGBoost       test             15        9886             2118       2119  9.767157 12.360691 -0.002108
```

## Validation-based model selection
```text
dataset                   target selected_by_validation_mae  validation_mae                                                                                               saved_pipeline
batting          next_match_runs           LinearRegression       15.864845          D:\Git\Personal\ipl-player-performance\models\day8\batting_next_match_runs_selected_pipeline.joblib
bowling       next_match_wickets           LinearRegression        0.789086       D:\Git\Personal\ipl-player-performance\models\day8\bowling_next_match_wickets_selected_pipeline.joblib
bowling next_match_runs_conceded                    XGBoost        8.490233 D:\Git\Personal\ipl-player-performance\models\day8\bowling_next_match_runs_conceded_selected_pipeline.joblib
```

## Outputs
- `reports/day8/feature_eligibility_review.csv`
- `reports/day8/chronological_split_summary.csv`
- `reports/day8/model_comparison_metrics.csv`
- `reports/day8/validation_model_selection.csv`
- `models/day8/*_selected_pipeline.joblib` (when a model run succeeds)
- `docs/day8_tree_based_regression.md`

## Methodology and limitations
- Target variables: `next_match_runs`, `next_match_wickets`, and `next_match_runs_conceded`.
- Only numeric `prior_...` columns are automatic feature candidates.
- Uses chronological row split: 70% train, 15% validation, 15% test.
- Median imputation is fitted inside a pipeline on training rows only.
- Selection uses validation MAE, with validation RMSE as tie-breaker; test scores do not select the model.
- The split is row-based, so a match can cross split boundaries; inspect dates and consider group-based splits before final reporting.
- XGBoost is skipped if the package cannot be imported; this does not stop Random Forest.
- The saved pipeline is trained on the training split only and is not the final production artifact.
- No metric is asserted until the notebook runs successfully against the actual project files.

## Next step
Day 9: evaluate errors, inspect feature importance, and decide a leakage-safe final training strategy.
