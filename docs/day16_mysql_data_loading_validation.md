# Day 16 — MySQL Data Loading and Validation

- **Run started:** 2026-10-21T19:01:58+05:30
- **Project root:** `D:\Git\Personal\ipl-player-performance`
- **Overall status:** **PASS**
- **MySQL version:** `8.0.46`

## Objective
Load the three processed CSV datasets into dedicated MySQL staging tables and validate the load without modifying final production tables.

## Check summary
| check             | status |
| ----------------- | ------ |
| mysql_connection  | PASS   |
| all_staging_loads | PASS   |
| row_counts        | PASS   |
| column_order      | PASS   |
| candidate_keys    | PASS   |

## Source file audit
| dataset              | path                                                                           | exists | rows  | columns | duplicate_rows | missing_cells | status |
| -------------------- | ------------------------------------------------------------------------------ | ------ | ----- | ------- | -------------- | ------------- | ------ |
| batting_player_match | D:\Git\Personal\ipl-player-performance\data\processed\batting_player_match.csv | True   | 18768 | 24      | 0              | 23666         | LOADED |
| bowling_player_match | D:\Git\Personal\ipl-player-performance\data\processed\bowling_player_match.csv | True   | 14700 | 24      | 0              | 15295         | LOADED |
| match_metadata       | D:\Git\Personal\ipl-player-performance\data\processed\match_metadata.csv       | True   | 1243  | 9       | 0              | 1294          | LOADED |

## Candidate key checks
| dataset              | candidate_key          | resolved_columns       | null_key_rows | duplicate_key_rows | status |
| -------------------- | ---------------------- | ---------------------- | ------------- | ------------------ | ------ |
| batting_player_match | match_id + player_name | match_id + player_name | 0             | 0                  | PASS   |
| bowling_player_match | match_id + player_name | match_id + player_name | 0             | 0                  | PASS   |
| match_metadata       | match_id               | match_id               | 0             | 0                  | PASS   |

## Staging load status
| dataset              | table_name                   | source_rows | status | error |
| -------------------- | ---------------------------- | ----------- | ------ | ----- |
| batting_player_match | stg_ipl_batting_player_match | 18768       | LOADED |       |
| bowling_player_match | stg_ipl_bowling_player_match | 14700       | LOADED |       |
| match_metadata       | stg_ipl_match_metadata       | 1243        | LOADED |       |

## Database validation
| dataset              | table_name                   | source_rows | database_rows | row_count_match | source_column_count | database_column_count | column_order_match | status |
| -------------------- | ---------------------------- | ----------- | ------------- | --------------- | ------------------- | --------------------- | ------------------ | ------ |
| batting_player_match | stg_ipl_batting_player_match | 18768       | 18768         | True            | 24                  | 24                    | True               | PASS   |
| bowling_player_match | stg_ipl_bowling_player_match | 14700       | 14700         | True            | 24                  | 24                    | True               | PASS   |
| match_metadata       | stg_ipl_match_metadata       | 1243        | 1243          | True            | 9                   | 9                     | True               | PASS   |

## Outputs generated
- `reports/day16/source_file_audit.csv`
- `reports/day16/candidate_key_checks.csv`
- `reports/day16/staging_load_status.csv`
- `reports/day16/database_validation.csv`
- `sql/day16_mysql_staging_validation.sql`
- `docs/day16_mysql_data_loading_validation.md`

## Interpretation and limitations
- Staging tables are temporary integration targets; they are not yet the final curated schema.
- Candidate key results are diagnostic. Duplicate rows are not deleted automatically.
- Row-count equality confirms record counts, not full semantic correctness.
- Pandas infers SQL column types; a reviewed production schema and explicit constraints should be established before promoting data.
- This notebook does not train models, create Django endpoints, or configure AWS.

## Next steps
Review candidate-key issues and schema types, then define/implement the final MySQL schema and Django database integration in the next project day.
