from django.db import connection
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Table and column names detected from the MySQL staging schema.
BATTING_TABLE = 'stg_ipl_batting_player_match'
BOWLING_TABLE = 'stg_ipl_bowling_player_match'
BAT_NAME = 'player_name'
BOWL_NAME = 'player_name'
BAT_RUNS = 'runs'
BAT_MATCH = 'match_id'
BAT_BALLS = 'balls_faced'
BAT_FOURS = 'fours'
BAT_SIXES = 'sixes'
BOWL_WICKETS = 'wickets'
BOWL_RUNS = 'runs_conceded'
BOWL_OVERS = 'overs'
BOWL_MATCH = 'match_id'

def q(identifier):
    if not identifier or not identifier.replace("_", "").isalnum():
        raise ValueError("Unsafe database identifier")
    return "`" + identifier.replace("`", "``") + "`"

def fetch_all(sql, params=None):
    with connection.cursor() as cursor:
        cursor.execute(sql, params or [])
        columns = [col[0] for col in cursor.description] if cursor.description else []
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def number(value):
    if value is None:
        return 0
    try:
        return float(value) if "." in str(value) else int(value)
    except (TypeError, ValueError):
        return value

class PlayerListAPIView(APIView):
    def get(self, request):
        search = (request.query_params.get("search") or "").strip()
        try:
            page = max(1, int(request.query_params.get("page", 1)))
            page_size = min(100, max(1, int(request.query_params.get("page_size", 25))))
        except ValueError:
            return Response({"detail": "page and page_size must be integers."},
                            status=status.HTTP_400_BAD_REQUEST)
        union_sql = (
            f"SELECT {q(BAT_NAME)} AS player_name FROM {q(BATTING_TABLE)} "
            f"WHERE {q(BAT_NAME)} IS NOT NULL AND TRIM(CAST({q(BAT_NAME)} AS CHAR)) <> '' "
            f"UNION SELECT {q(BOWL_NAME)} AS player_name FROM {q(BOWLING_TABLE)} "
            f"WHERE {q(BOWL_NAME)} IS NOT NULL AND TRIM(CAST({q(BOWL_NAME)} AS CHAR)) <> ''"
        )
        filter_sql = " WHERE player_name LIKE %s" if search else ""
        params = [f"%{search}%"] if search else []
        count_rows = fetch_all(
            f"SELECT COUNT(*) AS total FROM ({union_sql}) AS all_players{filter_sql}", params
        )
        total = int(count_rows[0]["total"]) if count_rows else 0
        offset = (page - 1) * page_size
        results = fetch_all(
            f"SELECT player_name FROM ({union_sql}) AS all_players{filter_sql} "
            "GROUP BY player_name ORDER BY player_name LIMIT %s OFFSET %s",
            params + [page_size, offset],
        )
        return Response({"count": total, "page": page, "page_size": page_size,
                         "total_pages": (total + page_size - 1) // page_size, "results": results})

class PlayerDetailAPIView(APIView):
    def get(self, request, player_name):
        bat_fields = ["COUNT(*) AS batting_records"]
        if BAT_MATCH: bat_fields.append(f"COUNT(DISTINCT {q(BAT_MATCH)}) AS matches")
        if BAT_RUNS: bat_fields.append(f"COALESCE(SUM({q(BAT_RUNS)}), 0) AS runs")
        if BAT_BALLS: bat_fields.append(f"COALESCE(SUM({q(BAT_BALLS)}), 0) AS balls_faced")
        if BAT_FOURS: bat_fields.append(f"COALESCE(SUM({q(BAT_FOURS)}), 0) AS fours")
        if BAT_SIXES: bat_fields.append(f"COALESCE(SUM({q(BAT_SIXES)}), 0) AS sixes")
        batting_rows = fetch_all(
            f"SELECT {', '.join(bat_fields)} FROM {q(BATTING_TABLE)} WHERE {q(BAT_NAME)} = %s",
            [player_name])
        batting = batting_rows[0] if batting_rows else {"batting_records": 0}
        bowl_fields = ["COUNT(*) AS bowling_records"]
        if BOWL_MATCH: bowl_fields.append(f"COUNT(DISTINCT {q(BOWL_MATCH)}) AS matches")
        if BOWL_WICKETS: bowl_fields.append(f"COALESCE(SUM({q(BOWL_WICKETS)}), 0) AS wickets")
        if BOWL_RUNS: bowl_fields.append(f"COALESCE(SUM({q(BOWL_RUNS)}), 0) AS runs_conceded")
        if BOWL_OVERS: bowl_fields.append(f"COALESCE(SUM({q(BOWL_OVERS)}), 0) AS overs")
        bowling_rows = fetch_all(
            f"SELECT {', '.join(bowl_fields)} FROM {q(BOWLING_TABLE)} WHERE {q(BOWL_NAME)} = %s",
            [player_name])
        bowling = bowling_rows[0] if bowling_rows else {"bowling_records": 0}
        if int(batting.get("batting_records", 0)) == 0 and int(bowling.get("bowling_records", 0)) == 0:
            raise Http404("Player not found.")
        for section in (batting, bowling):
            for key, value in list(section.items()):
                section[key] = number(value)
        return Response({"player_name": player_name, "batting": batting, "bowling": bowling})
