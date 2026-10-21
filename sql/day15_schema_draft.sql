-- Day 15 schema draft: review before applying.
-- This notebook does not execute this DDL.
CREATE TABLE IF NOT EXISTS matches (
    match_id TEXT PRIMARY KEY,
    match_date DATE,
    season TEXT,
    team1 TEXT,
    team2 TEXT,
    venue TEXT
);
CREATE TABLE IF NOT EXISTS batting_player_match (
    match_id TEXT NOT NULL REFERENCES matches(match_id),
    player_name TEXT NOT NULL,
    team TEXT,
    runs INTEGER,
    balls_faced INTEGER,
    fours INTEGER,
    sixes INTEGER,
    strike_rate DOUBLE PRECISION,
    PRIMARY KEY (match_id, player_name)
);
CREATE TABLE IF NOT EXISTS bowling_player_match (
    match_id TEXT NOT NULL REFERENCES matches(match_id),
    player_name TEXT NOT NULL,
    team TEXT,
    wickets INTEGER,
    runs_conceded INTEGER,
    legal_balls INTEGER,
    economy DOUBLE PRECISION,
    PRIMARY KEY (match_id, player_name)
);
CREATE INDEX IF NOT EXISTS idx_matches_match_date ON matches(match_date);
CREATE INDEX IF NOT EXISTS idx_batting_player_name ON batting_player_match(player_name);
CREATE INDEX IF NOT EXISTS idx_bowling_player_name ON bowling_player_match(player_name);
