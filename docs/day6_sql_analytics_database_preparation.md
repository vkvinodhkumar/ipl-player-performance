# Day 6: SQL Analytics and Database Preparation

## Input dataset shapes
- matches: 1,243 rows x 9 columns\n- batting: 18,768 rows x 24 columns\n- bowling: 14,700 rows x 24 columns\n- batting_features: 18,030 rows x 49 columns\n- bowling_features: 14,123 rows x 50 columns

## Input validation
```text
dataset                                 check  issue_count status note
matches                      missing match_id            0   PASS     
batting                      missing match_id            0   PASS     
bowling                      missing match_id            0   PASS     
matches               duplicate match_id rows            0   PASS     
batting                   missing player_name            0   PASS     
batting duplicate match_id + player_name rows            0   PASS     
bowling                   missing player_name            0   PASS     
bowling duplicate match_id + player_name rows            0   PASS     
```

## Schema mapping review
```text
dataset  database_column  present_in_csv                          action
matches         match_id            True           map after type review
matches             date            True           map after type review
matches           season            True           map after type review
matches            venue            True           map after type review
matches             city            True           map after type review
matches           team_1            True           map after type review
matches           team_2            True           map after type review
matches      source_file            True           map after type review
matches       match_type            True           map after type review
batting         match_id            True           map after type review
batting      player_name            True           map after type review
batting        player_id            True           map after type review
batting             date            True           map after type review
batting           season            True           map after type review
batting             team            True           map after type review
batting       opposition            True           map after type review
batting             runs            True           map after type review
batting      balls_faced            True           map after type review
batting            fours            True           map after type review
batting            sixes            True           map after type review
batting      strike_rate            True           map after type review
batting batting_position            True           map after type review
batting        dismissed           False not available; do not fabricate
bowling         match_id            True           map after type review
bowling      player_name            True           map after type review
bowling        player_id            True           map after type review
bowling             date            True           map after type review
bowling           season            True           map after type review
bowling             team            True           map after type review
bowling       opposition            True           map after type review
bowling          wickets            True           map after type review
bowling    runs_conceded            True           map after type review
bowling      legal_balls            True           map after type review
bowling            overs            True           map after type review
bowling          economy            True           map after type review
bowling          maidens           False not available; do not fabricate
bowling             dots            True           map after type review
bowling            wides            True           map after type review
bowling          noballs            True           map after type review
```

## Files generated
- `sql/day6_schema.sql`
- `sql/top_batters_by_runs.sql`
- `sql/top_bowlers_by_wickets.sql`
- `sql/season_team_batting.sql`
- `sql/player_recent_form.sql`
- `sql/bowling_economy.sql`
- `reports/day6/database_input_validation.csv`
- `reports/day6/schema_mapping_review.csv`

## Database safety
- Database loading is optional.
- No table is dropped by this notebook.
- Review DDL and mappings before execution.
- SQL query files are templates until run against a populated database.

## Limitations
- No ML/DL model is trained on Day 6.
- A database connection is not confirmed unless a live connection succeeds.

## Next step
Day 7: review feature eligibility, missingness and leakage safeguards before baseline modelling.
