SELECT player_name,
       SUM(runs_conceded) AS runs_conceded,
       SUM(legal_balls) AS legal_balls,
       CASE WHEN SUM(legal_balls) > 0
            THEN ROUND(6.0 * SUM(runs_conceded) / SUM(legal_balls), 2)
            ELSE NULL END AS economy_rate
FROM bowling_player_match
GROUP BY player_name
ORDER BY (economy_rate IS NULL), economy_rate ASC;
