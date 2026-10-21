# Day 18 — Player List and Player Detail APIs\n\n## Environment\n- Django engine: `django.db.backends.mysql`\n- Database: `ipl_analytics`\n- MySQL version: `8.0.46`\n\n## Detected staging schema\ndataset                        table           column data_type
batting stg_ipl_batting_player_match         match_id    bigint
batting stg_ipl_batting_player_match             date      text
batting stg_ipl_batting_player_match           season      text
batting stg_ipl_batting_player_match            venue      text
batting stg_ipl_batting_player_match             city      text
batting stg_ipl_batting_player_match           team_1      text
batting stg_ipl_batting_player_match           team_2      text
batting stg_ipl_batting_player_match       match_type    double
batting stg_ipl_batting_player_match             team      text
batting stg_ipl_batting_player_match       opposition      text
batting stg_ipl_batting_player_match      player_name      text
batting stg_ipl_batting_player_match        player_id      text
batting stg_ipl_batting_player_match player_name_norm      text
batting stg_ipl_batting_player_match        team_norm      text
batting stg_ipl_batting_player_match  opposition_norm      text
batting stg_ipl_batting_player_match             runs    bigint
batting stg_ipl_batting_player_match      balls_faced    bigint
batting stg_ipl_batting_player_match            fours    bigint
batting stg_ipl_batting_player_match            sixes    bigint
batting stg_ipl_batting_player_match batting_position    bigint
batting stg_ipl_batting_player_match    was_dismissed   tinyint
batting stg_ipl_batting_player_match   dismissal_kind      text
batting stg_ipl_batting_player_match    innings_count    bigint
batting stg_ipl_batting_player_match      strike_rate    double
bowling stg_ipl_bowling_player_match         match_id    bigint
bowling stg_ipl_bowling_player_match             date      text
bowling stg_ipl_bowling_player_match           season      text
bowling stg_ipl_bowling_player_match            venue      text
bowling stg_ipl_bowling_player_match             city      text
bowling stg_ipl_bowling_player_match           team_1      text
bowling stg_ipl_bowling_player_match           team_2      text
bowling stg_ipl_bowling_player_match       match_type    double
bowling stg_ipl_bowling_player_match             team      text
bowling stg_ipl_bowling_player_match       opposition      text
bowling stg_ipl_bowling_player_match      player_name      text
bowling stg_ipl_bowling_player_match        player_id      text
bowling stg_ipl_bowling_player_match player_name_norm      text
bowling stg_ipl_bowling_player_match        team_norm      text
bowling stg_ipl_bowling_player_match  opposition_norm      text
bowling stg_ipl_bowling_player_match      legal_balls    bigint
bowling stg_ipl_bowling_player_match    runs_conceded    bigint
bowling stg_ipl_bowling_player_match          wickets    bigint
bowling stg_ipl_bowling_player_match            wides    bigint
bowling stg_ipl_bowling_player_match          noballs    bigint
bowling stg_ipl_bowling_player_match             dots    bigint
bowling stg_ipl_bowling_player_match    innings_count    bigint
bowling stg_ipl_bowling_player_match            overs    double
bowling stg_ipl_bowling_player_match          economy    double\n\n## Source counts\ndataset                        table  rows  distinct_nonblank_players
batting stg_ipl_batting_player_match 18768                        738
bowling stg_ipl_bowling_player_match 14700                        577\n\n## Task status\n                        task               status
      Django project located                 PASS
            MySQL configured                 PASS
   MySQL connection verified                 PASS
   Staging schemas inspected                 PASS
Player-name columns detected                 PASS
             Views generated                 PASS
        App routes generated                 PASS
          ipl_api registered                 PASS
  Project URL include merged PENDING MANUAL CHECK
         Django system check                 PASS\n\n## Endpoints\n- `GET /api/players/?search=<name>&page=1&page_size=25`\n- `GET /api/players/<player_name>/`\n\n## Manual integration\n- Ensure `ipl_api` is in `INSTALLED_APPS`.\n- Merge `django_api/config/day18_urls_patch.txt` into project URLs.\n- No migrations were run.\n