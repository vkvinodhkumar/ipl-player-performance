SELECT player_name, SUM(runs) AS total_runs,
       ROUND(AVG(runs), 2) AS average_runs_per_match
FROM batting_player_match
GROUP BY player_name
ORDER BY total_runs DESC
LIMIT 20;
