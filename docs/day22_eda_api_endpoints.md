# Day 22 — EDA API Endpoints

- Generated: 2026-10-21T23:49:15
- Schema inspection return code: **0**
- Django check return code: **0**
- Day 21 regression test return code: **0**

## Schema inspection

```text
{"stg_ipl_batting_player_match": [{"column": "match_id", "data_type": "bigint", "nullable": "YES"}, {"column": "date", "data_type": "text", "nullable": "YES"}, {"column": "season", "data_type": "text", "nullable": "YES"}, {"column": "venue", "data_type": "text", "nullable": "YES"}, {"column": "city", "data_type": "text", "nullable": "YES"}, {"column": "team_1", "data_type": "text", "nullable": "YES"}, {"column": "team_2", "data_type": "text", "nullable": "YES"}, {"column": "match_type", "data_type": "double", "nullable": "YES"}, {"column": "team", "data_type": "text", "nullable": "YES"}, {"column": "opposition", "data_type": "text", "nullable": "YES"}, {"column": "player_name", "data_type": "text", "nullable": "YES"}, {"column": "player_id", "data_type": "text", "nullable": "YES"}, {"column": "player_name_norm", "data_type": "text", "nullable": "YES"}, {"column": "team_norm", "data_type": "text", "nullable": "YES"}, {"column": "opposition_norm", "data_type": "text", "nullable": "YES"}, {"column": "runs", "data_type": "bigint", "nullable": "YES"}, {"column": "balls_faced", "data_type": "bigint", "nullable": "YES"}, {"column": "fours", "data_type": "bigint", "nullable": "YES"}, {"column": "sixes", "data_type": "bigint", "nullable": "YES"}, {"column": "batting_position", "data_type": "bigint", "nullable": "YES"}, {"column": "was_dismissed", "data_type": "tinyint", "nullable": "YES"}, {"column": "dismissal_kind", "data_type": "text", "nullable": "YES"}, {"column": "innings_count", "data_type": "bigint", "nullable": "YES"}, {"column": "strike_rate", "data_type": "double", "nullable": "YES"}], "stg_ipl_bowling_player_match": [{"column": "match_id", "data_type": "bigint", "nullable": "YES"}, {"column": "date", "data_type": "text", "nullable": "YES"}, {"column": "season", "data_type": "text", "nullable": "YES"}, {"column": "venue", "data_type": "text", "nullable": "YES"}, {"column": "city", "data_type": "text", "nullable": "YES"}, {"column": "team_1", "data_type": "text", "nullable": "YES"}, {"column": "team_2", "data_type": "text", "nullable": "YES"}, {"column": "match_type", "data_type": "double", "nullable": "YES"}, {"column": "team", "data_type": "text", "nullable": "YES"}, {"column": "opposition", "data_type": "text", "nullable": "YES"}, {"column": "player_name", "data_type": "text", "nullable": "YES"}, {"column": "player_id", "data_type": "text", "nullable": "YES"}, {"column": "player_name_norm", "data_type": "text", "nullable": "YES"}, {"column": "team_norm", "data_type": "text", "nullable": "YES"}, {"column": "opposition_norm", "data_type": "text", "nullable": "YES"}, {"column": "legal_balls", "data_type": "bigint", "nullable": "YES"}, {"column": "runs_conceded", "data_type": "bigint", "nullable": "YES"}, {"column": "wickets", "data_type": "bigint", "nullable": "YES"}, {"column": "wides", "data_type": "bigint", "nullable": "YES"}, {"column": "noballs", "data_type": "bigint", "nullable": "YES"}, {"column": "dots", "data_type": "bigint", "nullable": "YES"}, {"column": "innings_count", "data_type": "bigint", "nullable": "YES"}, {"column": "overs", "data_type": "double", "nullable": "YES"}, {"column": "economy", "data_type": "double", "nullable": "YES"}], "stg_ipl_match_metadata": [{"column": "match_id", "data_type": "bigint", "nullable": "YES"}, {"column": "source_file", "data_type": "text", "nullable": "YES"}, {"column": "date", "data_type": "text", "nullable": "YES"}, {"column": "season", "data_type": "text", "nullable": "YES"}, {"column": "venue", "data_type": "text", "nullable": "YES"}, {"column": "city", "data_type": "text", "nullable": "YES"}, {"column": "team_1", "data_type": "text", "nullable": "YES"}, {"column": "team_2", "data_type": "text", "nullable": "YES"}, {"column": "match_type", "data_type": "double", "nullable": "YES"}]}

```

## Django check

```text
System check identified no issues (0 silenced).

```

## Regression test

```text
Found 6 test(s).
System check identified no issues (0 silenced).

......
----------------------------------------------------------------------
Ran 6 tests in 0.001s

OK
```

## Endpoint plan

- `GET /api/eda/summary/` — Counts and overall batting/bowling totals. Dependency: player-match and metadata tables.
- `GET /api/eda/batting/` — Runs, balls, boundaries, strike rate; grouped by player. Dependency: batting staging table.
- `GET /api/eda/bowling/` — Wickets, runs conceded, overs, economy; grouped by player. Dependency: bowling staging table.
- `GET /api/eda/season/` — Season-wise totals/trends. Dependency: requires confirmed season/date field or match metadata join.
- `GET /api/eda/venue/` — Venue-wise totals/trends. Dependency: requires confirmed venue field in metadata.
- `GET /api/eda/opposition/` — Player performance against opposition. Dependency: requires confirmed opposition/team fields and join.
- `GET /api/eda/recent-form/` — Last 5 chronological player-match records. Dependency: requires confirmed date/sequence field.

## Implementation status

This notebook inspects the real MySQL schema and records an endpoint plan. It intentionally does not overwrite views.py or urls.py. Implement the schema-dependent endpoints only after reviewing `mysql_staging_schema.csv` and confirming date, season, venue, team, and opposition columns.
