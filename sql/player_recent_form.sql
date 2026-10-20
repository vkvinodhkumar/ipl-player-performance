SELECT player_name, date, match_id, runs
FROM (
    SELECT player_name, date, match_id, runs,
           ROW_NUMBER() OVER (
               PARTITION BY player_name ORDER BY date DESC, match_id DESC
           ) AS rn
    FROM batting_player_match
) ranked
WHERE rn <= 5
ORDER BY player_name, date DESC;\n