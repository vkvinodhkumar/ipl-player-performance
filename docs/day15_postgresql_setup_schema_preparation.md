# Day 15 — PostgreSQL Setup and Schema Preparation

- **Generated:** 2026-10-21T15:43:50+05:30
- **Project root:** `D:\Git\Personal\ipl-player-performance`
- **Overall status:** **REVIEW**

## Input file status
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
          table_name        candidate_key  duplicate_key_rows  null_key_rows status
batting_player_match match_id+player_name                   0              0   PASS
bowling_player_match match_id+player_name                   0              0   PASS
      match_metadata             match_id                   0              0   PASS
```

## Schema draft
- **Status:** GENERATED — review column mappings/types before use
- **Path:** `D:\Git\Personal\ipl-player-performance\sql\day15_schema_draft.sql`
- **Blockers:** None detected by the current checks.

The DDL is a starter draft, not a guarantee that all source columns are mapped. Review the real CSV columns and intended data types before applying it. Confirm that each player appears at most once per match in each player-match table.

## PostgreSQL connection
- **Status:** FAIL
- **Server version:** Not available
- **Error:** OperationalError: (psycopg.errors.ConnectionTimeout) connection timeout expired
Multiple connection attempts failed. All failures were:
- host: 'localhost', port: 5432, hostaddr: '::1': connection timeout expired
- host: 'localhost', port: 5432, hostaddr: '127.0.0.1': connection timeout expired
(Background on this error at: https://sqlalche.me/e/21/e3q8)

The notebook runs only `SELECT 1` and `SELECT version()`. No tables are created and no records are inserted.

## Generated files
- `reports/day15/input_status.csv`
- `reports/day15/source_schema_review.csv`
- `reports/day15/candidate_key_checks.csv`
- `reports/day15/task_status.csv`
- `sql/day15_schema_draft.sql` (only if key checks pass)
- `docs/day15_postgresql_setup_schema_preparation.md`

## Next steps
1. Resolve missing inputs and key-check failures.
2. Review and correct the DDL against the actual source schema.
3. Configure PostgreSQL credentials with an environment variable.
4. Apply the reviewed schema using a controlled/manual step.
5. Next, prepare safe, repeatable data loading with duplicate handling and row-count validation.

## Limitations
This report reflects only the inputs and database connection available during this notebook run. A passing connection test does not mean the schema has been applied or the data has been loaded.
