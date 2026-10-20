# Project Decision Log

## Day 1: Source audit
1. Cricsheet IPL JSON is the primary historical source.
2. Supplied 2026 CSV files are a processed/reference source.
3. Raw source files remain unchanged.
4. Duplicate rows require investigation before any deduplication.
5. Reconcile the 2026 match directories with `fixtures.csv`.
6. Preserve original player and team labels; use normalized values only for matching.
7. Do not invent player IDs, features, or model results.
8. Do not train models during the source-audit stage.
9. Enforce chronological features and targets to prevent leakage.

## Day 2
Day 2 decisions are recorded in `day2_data_ingestion_validation.md` after the Day 2 notebook has been run and reviewed.
