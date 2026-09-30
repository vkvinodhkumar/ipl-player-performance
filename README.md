# IPL Player Performance Analytics and Prediction

Capstone Project 2 covering IPL batting and bowling analytics, EDA, SQL, machine learning, deep learning, Django REST APIs, batch testing, Power BI, and AWS deployment.

## Day 1 Status

Dataset audit and project scaffolding completed for Day 1. No model training is performed on Day 1.

## Data Sources

- Cricsheet IPL male JSON archive
- Supplied 2026 processed IPL CSV archive

The actual schemas are audited before feature engineering. No feature, target, player ID, or model result is assumed without evidence from the supplied data.

## Reproducibility

Configuration is supplied through `.env`. Local and AWS environments use the same application configuration pattern with different environment variables.

## Planned Pipeline

Extract → Validate → Clean → Transform → Player-Match Dataset → PostgreSQL → EDA/SQL → Features → ML/DL → Django REST API → Power BI/AWS

See `docs/day1_dataset_audit.md` for the Day 1 audit.
