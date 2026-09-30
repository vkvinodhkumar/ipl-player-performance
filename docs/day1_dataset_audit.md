# Day 1 Dataset Audit

## Project

**IPL Player Performance Analytics and Prediction Using Machine Learning and Deep Learning**

## Audit Date

2026-09-30

## Source Archives

| Archive | Compressed size | Uncompressed size | Contents |
|---|---:|---:|---|
| `ipl_male_json.zip` | 4.94 MB | 100.70 MB | Cricsheet IPL male JSON |
| `2026.zip` | 0.81 MB | 2.54 MB | 2026 processed CSV dataset |
| **Combined** | **5.75 MB** | **103.24 MB** | Both supplied sources |

The combined supplied dataset is below the project's 500 MB requirement.

## 1. Cricsheet Audit

- JSON match files: **1,243**
- Match type: **T20** for all 1,243 files
- Date range: **2008-04-18 to 2026-05-31**
- Unique player names found in `info.players`: **811**
- Unique teams: **19**
- Registry person IDs present: **966**
- Seasons represented: **2007/08 through 2026**
- Top-level JSON keys: `meta`, `info`, `innings`
- `info` contains match metadata including dates, teams, venue, season, players, registry, toss and outcome.
- `innings` contains delivery-level batting/bowling information.

### Cricsheet season counts

| Season | Matches |
|---|---:|
| 2007/08 | 58 |
| 2009 | 57 |
| 2009/10 | 60 |
| 2011 | 73 |
| 2012 | 74 |
| 2013 | 76 |
| 2014 | 60 |
| 2015 | 59 |
| 2016 | 60 |
| 2017 | 59 |
| 2018 | 60 |
| 2019 | 60 |
| 2020/21 | 60 |
| 2021 | 60 |
| 2022 | 74 |
| 2023 | 74 |
| 2024 | 71 |
| 2025 | 74 |
| 2026 | 74 |

**Important:** The Cricsheet archive is the authoritative historical delivery-level source for this project. We should not use the 2026 processed archive as the only historical source because it contains only the 2026 season.

## 2. 2026 Processed Dataset Audit

The archive contains **74 match directories**.

### Fixture file

`2026/fixtures.csv`

- Rows: **70**
- Columns: `match_number`, `date`, `venue`, `team_1`, `team_2`
- Date range in fixture file: **2026-03-28 to 2026-05-24**
- Missing values: **0**
- Duplicate rows: **0**
- Duplicate match numbers: **0**
- Teams: **10**

There are **74 actual 2026 match directories** but only **70 rows in `fixtures.csv`**. The final four matches are present in the supplied Cricsheet archive and match directories but are not represented by rows in the supplied fixture file. Therefore, Day 2 must derive match metadata from the match-level source rather than assuming `fixtures.csv` is complete.

### Ball-by-ball

74 files, **17,523 rows**.

Columns:

`innings`, `team`, `over`, `ball`, `batter`, `bowler`, `non_striker`, `batter_runs`, `extra_runs`, `total_runs`, `is_boundary`, `non_boundary_run`, `extra_type`, `wides`, `noballs`, `byes`, `legbyes`, `penalty`, `is_wicket`, `wicket_kind`, `player_out`, `fielder`, `phase`

Observed missing values are concentrated in nullable event fields such as `extra_type`, `wicket_kind`, `player_out`, and `fielder`. These are structurally expected for deliveries where the corresponding event did not occur.

**Data-quality finding:** 51 exact duplicate rows occur across 36 match-level ball-by-ball files. These must be investigated in Day 2 before cleaning. They must not be silently removed without understanding whether they represent duplicated source records or legitimate repeated delivery representations.

### Batting scorecards

74 files, **1,130 rows**.

Columns:

`innings`, `team`, `batter`, `runs`, `balls`, `fours`, `sixes`, `strike_rate`, `dismissal`, `batting_position`

- Unique batter names: **176**
- Total runs: **26,151**
- Missing values: **0** across the observed columns
- Duplicate complete rows: **0**

This source directly supports batting player-match aggregation and the `next_match_runs` target.

### Bowling scorecards

74 files, **854 rows**.

Columns:

`innings`, `team`, `bowler`, `overs`, `maidens`, `runs`, `wickets`, `economy`, `dots`, `wides`, `noballs`

- Unique bowler names: **125**
- Total wickets: **835**
- Total runs conceded recorded in scorecards: **27,125**
- Missing values: **0**
- Duplicate complete rows: **0**

This source directly supports bowling player-match aggregation and both bowling targets: `next_match_wickets` and `next_match_runs_conceded`.

### Partnerships

74 files, **1,007 rows**.

Columns:

`innings`, `team`, `wicket_number`, `batter_1`, `batter_1_runs`, `batter_1_balls`, `batter_2`, `batter_2_runs`, `batter_2_balls`, `extras`, `total_runs`, `total_balls`

No missing values or duplicate complete rows were observed in the audit.

### Phase summary

74 files, **434 rows**.

Columns:

`innings`, `team`, `phase`, `runs`, `wickets`, `balls`, `run_rate`, `boundaries`, `dots`

No missing values or duplicate complete rows were observed in the audit.

### Other 2026 files

| File type | Match files |
|---|---:|
| `fall_of_wickets.csv` | 74 |
| `substitutions.csv` | 73 |
| `reviews.csv` | 62 |
| `super_over.csv` | 1 |

These files may be used later only where they add validated features or match-context information.

## 3. Target Feasibility

All three proposed targets are feasible from the supplied data:

1. **`next_match_runs`** from chronological player batting records.
2. **`next_match_wickets`** from chronological player bowling records.
3. **`next_match_runs_conceded`** from chronological player bowling records.

The target for player-match record N will be the corresponding statistic from that player's next chronological match appearance, not the same match.

Rows without a subsequent player appearance will not have a future target and should not be used as supervised training rows for that target.

## 4. Last-5 Sequence Feasibility

The supplied Cricsheet archive contains sufficient historical match and delivery information to construct chronological player-match sequences.

For each prediction row, the Deep Learning input can use the player's previous five eligible match records. Players with fewer than five previous eligible matches require an explicit minimum-history rule and should not be padded with fabricated performance values.

## 5. Batting Data Support

Supported directly by:

- Cricsheet delivery data
- 2026 batting scorecards
- Batting runs
- Balls faced
- Fours
- Sixes
- Strike rate
- Batting position
- Dismissal
- Match/team context
- Venue/date/season metadata

Additional historical features must be created only from columns actually present in the source.

## 6. Bowling Data Support

Supported directly by:

- Cricsheet delivery data
- 2026 bowling scorecards
- Overs
- Maidens
- Runs conceded
- Wickets
- Economy
- Dot balls
- Wides
- No-balls
- Match/team context
- Venue/date/season metadata

## 7. Leakage Risks Identified for Later Days

The following must be enforced during Days 4-8:

- Target match performance cannot be used as an input feature.
- Rolling statistics must be shifted so that they contain only prior matches.
- Season aggregates must be calculated using information available before the prediction match.
- Venue/opposition aggregates must use prior observations only.
- Chronological train/validation/test splitting is mandatory.
- The final five-match sequence must contain only matches before the prediction match.
- No future 2026 playoff information may enter earlier 2026 training features.

## 8. Day 1 Project Setup

Created:

```text
ipl-player-performance/
├── data/
│   ├── raw/
│   │   ├── ipl_male_json.zip
│   │   └── 2026.zip
│   └── processed/
├── pipeline/
├── analytics/
├── ml/
│   ├── batting/
│   └── bowling/
├── dl/
│   ├── batting/
│   └── bowling/
├── models/
│   ├── batting/
│   ├── bowling/
│   └── preprocessing/
├── sql/
├── django_api/
│   ├── config/
│   └── api/
├── notebooks/
├── tests/
├── deployment/
├── scripts/
├── docs/
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

A Python virtual environment was created at `.venv`. The runtime used for this environment is Python 3.13.5. No project dependencies were installed or model training performed on Day 1.

**Compatibility decision:** before installing the ML/DL stack, Day 2 or the environment setup step should verify the project's selected Python version against the TensorFlow and XGBoost versions used. We should not assume that every package supports the environment equally.

## 9. Day 1 Decision Log

1. Use Cricsheet JSON as the primary historical source.
2. Use the supplied 2026 CSV archive as a processed/reference source and validation source.
3. Derive match metadata from the authoritative match data rather than relying exclusively on the incomplete 2026 fixture file.
4. Preserve raw archives unchanged under `data/raw/`.
5. Investigate the 51 duplicate ball-by-ball rows during Day 2 validation.
6. Do not invent player IDs. Cricsheet provides registry identifiers that can be used after the identity mapping is properly inspected.
7. Do not invent model features until the actual historical JSON fields are mapped.
8. Do not train models on Day 1.

## 10. Day 1 Conclusion

The supplied data is sufficient to proceed with the proposed IPL-only project. The historical Cricsheet archive provides 1,243 IPL matches across 2008-2026, and the 2026 processed archive provides structured scorecards and analytical files.

The major items requiring attention in Day 2 are:

- exact duplicate ball-by-ball records,
- player identity standardization,
- complete match metadata construction,
- schema normalization between Cricsheet JSON and 2026 CSV,
- validation rules for scorecard totals,
- and environment/package compatibility.

No model result or predictive performance has been generated or assumed.
