# Day 3: Player-Match Dataset Construction

## Outputs

- `data/processed/batting_player_match.csv`
- `data/processed/bowling_player_match.csv`
- `data/processed/match_metadata.csv`
- `data/processed/player_registry_observations.csv`
- `docs/day3_data_dictionary.csv`

## Source policy

Cricsheet JSON is the primary historical source. The supplied 2026 scorecards are used for comparison and validation, not automatically appended to the historical datasets.

## Aggregation keys

- Batting: one row per `match_id` + `player_name`.
- Bowling: one row per `match_id` + `player_name`.

Innings-level statistics are aggregated into player-match records.

## Identity policy

Original player names are preserved. Normalized names are comparison keys only. Player IDs come from the Cricsheet registry when available. Missing IDs are not fabricated.

## Metric definitions

- Batting runs: sum of `runs.batter`.
- Balls faced: excludes wides and no-balls under the current implementation.
- Fours and sixes: batter-scored boundaries, excluding marked non-boundary runs.
- Bowling runs conceded: batter runs + wides + no-balls.
- Legal balls: deliveries excluding wides and no-balls.
- Bowler wickets: excludes configured non-bowler-credit dismissal types.
- Overs: derived from legal balls. Use `legal_balls` for numeric calculations.

## Validation

- Match/player key uniqueness.
- Non-negative performance statistics.
- Populated match IDs and valid dates.
- Inspection of 2026 scorecard schemas.

## Limitations and next checks

1. Compare derived 2026 statistics with scorecards using a verified match mapping.
2. Investigate failed validations before proceeding.
3. Review dismissal-kind and non-boundary edge cases.
4. Confirm balls-faced and bowler-credit rules.
5. Next-match targets belong to Day 4.
6. No ML/DL model is trained on Day 3.

## Row counts

- Cricsheet JSON matches processed: 1,243
- Batting player-match rows: 18,768
- Bowling player-match rows: 14,700
- Match metadata rows: 1,243
