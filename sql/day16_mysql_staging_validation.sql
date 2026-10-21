-- Day 16: read-only staging validation queries
-- Generated automatically from the Day 16 notebook.
SELECT COUNT(*) AS row_count FROM `stg_ipl_batting_player_match`;
SELECT COUNT(*) AS row_count FROM `stg_ipl_bowling_player_match`;
SELECT COUNT(*) AS row_count FROM `stg_ipl_match_metadata`;

-- Candidate duplicate-key check for batting_player_match
SELECT `match_id`, `player_name`, COUNT(*) AS occurrences
FROM `stg_ipl_batting_player_match`
GROUP BY `match_id`, `player_name`
HAVING COUNT(*) > 1
LIMIT 100;

-- Candidate duplicate-key check for bowling_player_match
SELECT `match_id`, `player_name`, COUNT(*) AS occurrences
FROM `stg_ipl_bowling_player_match`
GROUP BY `match_id`, `player_name`
HAVING COUNT(*) > 1
LIMIT 100;

-- Candidate duplicate-key check for match_metadata
SELECT `match_id`, COUNT(*) AS occurrences
FROM `stg_ipl_match_metadata`
GROUP BY `match_id`
HAVING COUNT(*) > 1
LIMIT 100;
