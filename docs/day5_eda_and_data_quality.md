# Day 5: Exploratory Data Analysis

## Dataset coverage

```text
                    dataset  rows  columns  unique_matches  unique_players   date_min   date_max
       batting_player_match 18768       24            1243           738.0 2008-04-18 2026-05-31
       bowling_player_match 14700       24            1243           577.0 2008-04-18 2026-05-31
             match_metadata  1243        9            1243             NaN 2008-04-18 2026-05-31
batting_next_match_features 18030       49            1240           633.0 2008-04-18 2026-05-29
bowling_next_match_features 14123       50            1240           503.0 2008-04-18 2026-05-29
```

## Key observations to investigate
- Review `missingness_report.csv` for columns with missing values.
- Review `duplicate_key_report.csv` for repeated match/player keys.
- Review `numeric_descriptive_statistics.csv` and boxplots for extreme values.
- Review `target_summary.csv` if Day 4 target tables were available.
- Do not remove outliers or impute missing values without a documented rule.

## Outputs
- `reports/day5/coverage_summary.csv`
- `reports/day5/missingness_report.csv`
- `reports/day5/duplicate_key_report.csv`
- `reports/day5/numeric_descriptive_statistics.csv`
- `reports/day5/target_summary.csv`

## Limitations
- Findings are descriptive and do not establish causality.
- No model is trained on Day 5.
- Verify suspected data-quality issues against source records before changing data.