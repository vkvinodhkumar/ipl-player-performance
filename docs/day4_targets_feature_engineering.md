# Day 4: Next-Match Targets and Feature Engineering

## Outputs
- `data/processed/batting_next_match_features.csv`
- `data/processed/bowling_next_match_features.csv`

## Target definitions
- Batting: `next_match_runs`, derived from the player's next chronological batting record.
- Bowling: `next_match_wickets` and `next_match_runs_conceded`, derived from the player's next chronological bowling record.

## Feature policy
- Player records sorted by date and match ID.
- Rolling means and cumulative averages use `shift(1)` so current-match performance is not included in historical features.
- The final record per player has no next-match target and is excluded from supervised output tables.
- Do not use current-match performance columns as predictors for the target on the same row.

## Validation
- Required input columns checked.
- Dates parsed and validated.
- Duplicate match/player keys checked.
- Match metadata join validated as many-to-one.
- Next-match target alignment checked.
- First player record has no prior-history values.
- Target date must not precede feature-row date.

## Row counts
- Batting input rows: 18,768
- Batting supervised rows: 18,030
- Batting unique players: 633
- Bowling input rows: 14,700
- Bowling supervised rows: 14,123
- Bowling unique players: 503

## Limitations and next checks
1. Confirm target semantics with the capstone supervisor.
2. Check same-day doubleheaders and match ordering where relevant.
3. Inspect missing/zero performance statistics and scorecard reconciliation.
4. Build chronological train/validation/test splits on the training days.
5. Compare Linear Regression, Random Forest, and XGBoost using MAE, RMSE, and R².
6. LSTM/GRU sequence modelling using the last five chronological matches is a later step.
7. No model is trained on Day 4.
