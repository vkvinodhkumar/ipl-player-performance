# Day 2: Data Ingestion and Validation

## Purpose
Investigate source coverage and duplicate records, reconcile 2026 match metadata with Cricsheet, inspect player identity observations, define validation checks, and create normalized 2026 match metadata.

## Source inventory
- Cricsheet JSON match files: 1,243
- 2026 match directories: 74
- Rows in `fixtures.csv`: 70
- Cricsheet 2026 matches identified from JSON: 74

## Duplicate investigation
- Files containing exact duplicate rows: 36
- Duplicate rows including repeated copies within those files: 99

### Decision
Do not remove duplicate rows automatically at this stage. Keep source data unchanged and investigate the repeated rows against source provenance and scorecard totals before implementing a deduplication rule.

## Match reconciliation
- Cricsheet 2026 matches absent from fixture match keys: 4
- Fixture rows absent from Cricsheet match keys: 0

Matching uses the match date and an unordered pair of normalized team names. Original source names are retained. Any unmatched rows or duplicate match keys must be inspected rather than silently discarded.

## Player identity audit
- Player-team observations: 27,909
- Unique player names: 811
- Unique non-null Cricsheet registry IDs: 809

Player names may have different spellings or formatting across sources. Preserve source names and only use normalized names for matching. Do not fabricate missing registry IDs.

## Normalized metadata output
- Output: `data/processed/match_metadata_2026.csv`
- Columns include Cricsheet match ID and filename, date, season, venue, city, original team labels, match type, normalized team labels, and a reconciliation key.

## Validation results
- Rows equal Cricsheet 2026 matches: PASS
- Unique match IDs: PASS
- No missing match IDs: PASS
- No missing dates: PASS
- No missing team 1: PASS
- No missing team 2: PASS
- Unique match keys: PASS

## Limitations and next checks
1. Review every failed validation before moving forward.
2. Inspect unmatched fixtures and Cricsheet matches.
3. Investigate duplicate groups and confirm whether they are source duplication or legitimate repeated deliveries.
4. Check whether the match key is unique for all source records.
5. Compare derived 2026 player-match statistics with scorecards after Day 3 dataset construction.
6. No machine-learning or deep-learning model is trained on Day 2.

## Next step
Day 3: construct one-row-per-player-per-match batting and bowling datasets from Cricsheet JSON, retain source provenance, document metric definitions, and validate keys and numeric ranges.
