SELECT season, team, SUM(runs) AS team_runs
FROM batting_player_match
GROUP BY season, team
ORDER BY season, team;\n