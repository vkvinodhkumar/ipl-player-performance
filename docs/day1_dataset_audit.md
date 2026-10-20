# Day 1: IPL Dataset Audit

## Project
IPL Player Performance Analytics and Prediction Using Machine Learning and Deep Learning.

## Purpose
Audit the extracted source files, inspect their schemas and coverage, identify data-quality risks, and decide which sources should be authoritative. This day is an audit only. It does not train machine-learning or deep-learning models.

## Source inventory

### Cricsheet IPL JSON
- JSON match files: 1,243
- Unique player names observed: 811
- Teams observed: 19
- Earliest date recorded in source metadata: 2008-04-18
- Latest date recorded in source metadata: 2026-05-31

### Supplied 2026 processed data
- Match directories: 74
- Rows in `fixtures.csv`: 70
- Ball-by-ball files: 74
- Combined ball-by-ball rows: 17,523
- Exact duplicate ball-by-ball rows detected: 51
- Batting scorecard files: 74
- Batting scorecard rows: 1,130
- Bowling scorecard files: 74
- Bowling scorecard rows: 854

## Findings and decisions
1. Use Cricsheet IPL JSON as the primary historical source.
2. Use the supplied 2026 CSV archive as a processed/reference source for schema and reconciliation checks.
3. Preserve raw extracted source files unchanged.
4. Do not remove duplicate ball-by-ball rows until their cause and impact have been investigated.
5. Reconcile match directories against `fixtures.csv`; fixture coverage may be incomplete.
6. Preserve original player and team labels. Normalized values are comparison keys, not replacements for source values.
7. Do not fabricate player identifiers or features.
8. Build future targets from chronologically later matches and prevent target leakage.
9. Do not train models on Day 1.

## Target feasibility
The intended regression targets are:
- `next_match_runs`
- `next_match_wickets`
- `next_match_runs_conceded`

The scorecard sources appear to contain the relevant current-match batting and bowling statistics needed to investigate these targets. Final target construction is deferred until player-match datasets and chronological ordering are established.

## Validation and limitations
This report records inventory and audit counts from the executed notebook variables. It does not assert that every source issue is resolved. Review notebook outputs for missing values, duplicate groups, schema differences, and any warnings before proceeding.

## Next step
Day 2: investigate duplicate records, reconcile 2026 match metadata against Cricsheet, inspect player registry identifiers, define validation rules, and save normalized match metadata.
