-- MySQL DDL DRAFT for IPL Player Performance Analytics
-- Review column types and keys against reports/day15/source_schema_review.csv.
-- This file is not executed by the notebook.
CREATE DATABASE IF NOT EXISTS ipl_analytics
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ipl_analytics;

CREATE TABLE IF NOT EXISTS batting_player_match (
  match_id VARCHAR(64) NOT NULL,
  player_name VARCHAR(255) NOT NULL,
  PRIMARY KEY (match_id, player_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS bowling_player_match (
  match_id VARCHAR(64) NOT NULL,
  player_name VARCHAR(255) NOT NULL,
  PRIMARY KEY (match_id, player_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Add remaining columns after reviewing the actual source schema.
-- Add match_metadata only after verifying its actual match identifier and uniqueness.
