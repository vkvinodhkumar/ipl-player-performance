SELECT player_name, SUM(wickets) AS total_wickets,
       SUM(runs_conceded) AS total_runs_conceded,
       SUM(legal_balls) AS total_legal_balls
FROM bowling_player_match
GROUP BY player_name
ORDER BY total_wickets DESC
LIMIT 20;\n