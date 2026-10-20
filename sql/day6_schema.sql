-- Day 6: PostgreSQL schema for IPL player performance
CREATE TABLE IF NOT EXISTS matches (
    match_id TEXT PRIMARY KEY,
    match_date DATE,
    season TEXT,
    venue TEXT,
    city TEXT,
    team_1 TEXT,
    team_2 TEXT,
    source_file TEXT,
    match_type TEXT
);

CREATE TABLE IF NOT EXISTS batting_player_match (
    match_id TEXT NOT NULL REFERENCES matches(match_id),
    player_name TEXT NOT NULL,
    player_id TEXT,
    date DATE,
    season TEXT,
    team TEXT,
    opposition TEXT,
    runs INTEGER,
    balls_faced INTEGER,
    fours INTEGER,
    sixes INTEGER,
    strike_rate DOUBLE PRECISION,
    batting_position INTEGER,
    dismissed BOOLEAN,
    PRIMARY KEY (match_id, player_name)
);

CREATE TABLE IF NOT EXISTS bowling_player_match (
    match_id TEXT NOT NULL REFERENCES matches(match_id),
    player_name TEXT NOT NULL,
    player_id TEXT,
    date DATE,
    season TEXT,
    team TEXT,
    opposition TEXT,
    wickets INTEGER,
    runs_conceded INTEGER,
    legal_balls INTEGER,
    overs TEXT,
    economy DOUBLE PRECISION,
    maidens INTEGER,
    dots INTEGER,
    wides INTEGER,
    noballs INTEGER,
    PRIMARY KEY (match_id, player_name)
);

CREATE INDEX IF NOT EXISTS idx_batting_player_date ON batting_player_match (player_name, date);
CREATE INDEX IF NOT EXISTS idx_bowling_player_date ON bowling_player_match (player_name, date);
CREATE INDEX IF NOT EXISTS idx_matches_date ON matches (match_date);
