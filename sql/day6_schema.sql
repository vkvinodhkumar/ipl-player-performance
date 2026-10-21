-- Day 6: MySQL schema for IPL player performance
CREATE TABLE IF NOT EXISTS matches (
    match_id VARCHAR(100) NOT NULL PRIMARY KEY,
    match_date DATE,
    season VARCHAR(32),
    venue VARCHAR(255),
    city VARCHAR(255),
    team_1 VARCHAR(255),
    team_2 VARCHAR(255),
    source_file VARCHAR(512),
    match_type VARCHAR(64),
    KEY idx_matches_date (match_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS batting_player_match (
    match_id VARCHAR(100) NOT NULL,
    player_name VARCHAR(255) NOT NULL,
    player_id VARCHAR(100),
    date DATE,
    season VARCHAR(32),
    team VARCHAR(255),
    opposition VARCHAR(255),
    runs INTEGER,
    balls_faced INTEGER,
    fours INTEGER,
    sixes INTEGER,
    strike_rate DOUBLE,
    batting_position INTEGER,
    dismissed BOOLEAN,
    PRIMARY KEY (match_id, player_name),
    KEY idx_batting_player_date (player_name, date),
    CONSTRAINT fk_batting_match FOREIGN KEY (match_id) REFERENCES matches(match_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS bowling_player_match (
    match_id VARCHAR(100) NOT NULL,
    player_name VARCHAR(255) NOT NULL,
    player_id VARCHAR(100),
    date DATE,
    season VARCHAR(32),
    team VARCHAR(255),
    opposition VARCHAR(255),
    wickets INTEGER,
    runs_conceded INTEGER,
    legal_balls INTEGER,
    overs VARCHAR(32),
    economy DOUBLE,
    maidens INTEGER,
    dots INTEGER,
    wides INTEGER,
    noballs INTEGER,
    PRIMARY KEY (match_id, player_name),
    KEY idx_bowling_player_date (player_name, date),
    CONSTRAINT fk_bowling_match FOREIGN KEY (match_id) REFERENCES matches(match_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
