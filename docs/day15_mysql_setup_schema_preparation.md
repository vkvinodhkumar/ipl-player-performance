# Day 15 — MySQL Setup and Schema Preparation

- Generated: 2026-10-23T21:32:26+05:30
- Project root: `D:\Git\Personal\ipl-player-performance`
- Python: 3.12.14
- Platform: Windows-11-10.0.26300-SP0

## Input status
```text
          input_name                                                                           path  exists  rows  columns read_error
batting_player_match D:\Git\Personal\ipl-player-performance\data\processed\batting_player_match.csv    True 18768       24       None
bowling_player_match D:\Git\Personal\ipl-player-performance\data\processed\bowling_player_match.csv    True 14700       24       None
      match_metadata       D:\Git\Personal\ipl-player-performance\data\processed\match_metadata.csv    True  1243        9       None
```

## Source schema review
```text
          table_name      column_name   dtype  null_count  distinct_non_null
batting_player_match         match_id   int64           0               1243
batting_player_match             date     str           0                947
batting_player_match           season     str           0                 19
batting_player_match            venue     str           0                 60
batting_player_match             city     str         746                 37
batting_player_match           team_1     str           0                 19
batting_player_match           team_2     str           0                 19
batting_player_match       match_type float64       18768                  0
batting_player_match             team     str           0                 19
batting_player_match       opposition     str           0                 19
batting_player_match      player_name     str           0                738
batting_player_match        player_id     str           0                736
batting_player_match player_name_norm     str           0                738
batting_player_match        team_norm     str           0                 19
batting_player_match  opposition_norm     str           0                 19
batting_player_match             runs   int64           0                136
batting_player_match      balls_faced   int64           0                 72
batting_player_match            fours   int64           0                 18
batting_player_match            sixes   int64           0                 15
batting_player_match batting_position   int64           0                 11
batting_player_match    was_dismissed    bool           0                  2
batting_player_match   dismissal_kind     str        4144                 17
batting_player_match    innings_count   int64           0                  2
batting_player_match      strike_rate float64           8               1428
bowling_player_match         match_id   int64           0               1243
bowling_player_match             date     str           0                947
bowling_player_match           season     str           0                 19
bowling_player_match            venue     str           0                 60
bowling_player_match             city     str         594                 37
bowling_player_match           team_1     str           0                 19
```

## Candidate key checks
```text
          table_name          candidate_key status                                            detail
batting_player_match match_id + player_name   PASS rows=18768, null_key_rows=0, duplicate_key_rows=0
bowling_player_match match_id + player_name   PASS rows=14700, null_key_rows=0, duplicate_key_rows=0
```

## DDL draft
- Status: `DRAFT_GENERATED_REVIEW_REQUIRED`
- File: `D:\Git\Personal\ipl-player-performance\sql\day15_mysql_schema_draft.sql`
- Blockers: None detected by basic checks

## MySQL connection
- Status: `PASS`
- Driver: `mysql+pymysql`
- Host: `localhost`
- Port: `3306`
- Database: `ipl_analytics`
- Server version: `8.0.46`
- Error: `None`

Connection check uses only `SELECT 1` and `SELECT VERSION()`. It does not create tables or insert data.

## Task status
```text
                             task                          status
Processed inputs present/readable                            PASS
                   Candidate keys                            PASS
                  MySQL DDL draft DRAFT_GENERATED_REVIEW_REQUIRED
                 MySQL connection                            PASS
          Documentation generated                            PASS
```

## Generated files
- `reports/day15/input_status.csv`
- `reports/day15/source_schema_review.csv`
- `reports/day15/candidate_key_checks.csv`
- `reports/day15/task_status.csv`
- `sql/day15_mysql_schema_draft.sql`
- `docs/day15_mysql_setup_schema_preparation.md`
