# Day 11 — Sequence Dataset Preparation

## Execution summary
### Validation checks
```text
dataset                   target  samples  sequence_length  feature_count status                                                                      detail
batting          next_match_runs    15821                5             15 REVIEW Feature tensor contains NaN/inf; fit imputation on training data in Day 12.
bowling       next_match_wickets    12335                5             15 REVIEW Feature tensor contains NaN/inf; fit imputation on training data in Day 12.
bowling next_match_runs_conceded    12335                5             15 REVIEW Feature tensor contains NaN/inf; fit imputation on training data in Day 12.
```

### Chronological splits
```text
dataset                   target      split  rows target_date_start target_date_end
batting          next_match_runs      train 11074        2008-05-03      2022-04-10
batting          next_match_runs validation  2373        2022-04-10      2024-04-29
batting          next_match_runs       test  2374        2024-04-29      2026-05-31
bowling       next_match_wickets      train  8634        2008-05-03      2022-04-02
bowling       next_match_wickets validation  1850        2022-04-02      2024-04-26
bowling       next_match_wickets       test  1851        2024-04-26      2026-05-31
bowling next_match_runs_conceded      train  8634        2008-05-03      2022-04-02
bowling next_match_runs_conceded validation  1850        2022-04-02      2024-04-26
bowling next_match_runs_conceded       test  1851        2024-04-26      2026-05-31
```

### Sequence manifest
```text
dataset                   target  sequence_length  feature_count  sample_count tensor_shape_json                                                                                                          tensor_path                                                                                                       metadata_path                                                                                                feature_manifest_path
batting          next_match_runs                5             15         15821    [15821, 5, 15]          D:\Git\Personal\ipl-player-performance\data\processed\day11_sequences\batting_next_match_runs_sequences.npz          D:\Git\Personal\ipl-player-performance\data\processed\day11_sequences\batting_next_match_runs_metadata.csv          D:\Git\Personal\ipl-player-performance\data\processed\day11_sequences\batting_next_match_runs_features.json
bowling       next_match_wickets                5             15         12335    [12335, 5, 15]       D:\Git\Personal\ipl-player-performance\data\processed\day11_sequences\bowling_next_match_wickets_sequences.npz       D:\Git\Personal\ipl-player-performance\data\processed\day11_sequences\bowling_next_match_wickets_metadata.csv       D:\Git\Personal\ipl-player-performance\data\processed\day11_sequences\bowling_next_match_wickets_features.json
bowling next_match_runs_conceded                5             15         12335    [12335, 5, 15] D:\Git\Personal\ipl-player-performance\data\processed\day11_sequences\bowling_next_match_runs_conceded_sequences.npz D:\Git\Personal\ipl-player-performance\data\processed\day11_sequences\bowling_next_match_runs_conceded_metadata.csv D:\Git\Personal\ipl-player-performance\data\processed\day11_sequences\bowling_next_match_runs_conceded_features.json
```

## Method
- Sequence length: 5 historical matches per sample.
- Input features: numeric `prior_...` columns only, saved in a per-target feature manifest.
- Target values: `next_match_runs`, `next_match_wickets`, and `next_match_runs_conceded`.
- Samples are ordered by player and historical match date; sequences do not cross player boundaries.
- The final historical row stores the next-match target.
- Train/validation/test partitions are ordered by target match date at 70% / 15% / 15%.
- No imputer or scaler is fitted during this dataset-preparation day.

## Outputs
- `data/processed/day11_sequences/*.npz`
- `data/processed/day11_sequences/*_metadata.csv`
- `data/processed/day11_sequences/*_features.json`
- `reports/day11/sequence_manifest.csv`
- `reports/day11/chronological_split_summary.csv`
- `reports/day11/sequence_validation_checks.csv`

## Limitations and review notes
- The `prior_` prefix is a screening convention, not proof that a feature is leakage-free.
- This is a sample-level chronological split; samples for different players in the same match can straddle boundaries.
- Missing input features are preserved as NaN so Day 12 can fit imputation only on training data.
- Sequence construction is based on rows present in the Day 4 player-match feature tables; verify that rows represent the intended player-match chronology and that next-match targets align correctly.

## Next
Day 12: train LSTM and GRU regressors with training-only preprocessing, early stopping where supported, and regression metrics.
