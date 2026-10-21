from django.db import connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Generated from Day 22 MySQL information_schema inspection.
CFG = {'bat_table': 'stg_ipl_batting_player_match', 'bowl_table': 'stg_ipl_bowling_player_match', 'meta_table': 'stg_ipl_match_metadata', 'player': 'player_name', 'runs': 'runs', 'balls': 'balls_faced', 'fours': 'fours', 'sixes': 'sixes', 'bat_match': 'match_id', 'wickets': 'wickets', 'runs_conceded': 'runs_conceded', 'overs': 'overs', 'bowl_match': 'match_id', 'date': 'date', 'season': 'season', 'venue': 'venue', 'team': None, 'opposition': None, 'meta_match': 'match_id'}

def qi(name):
    if not name or not str(name).replace("_", "").isalnum():
        raise ValueError("Invalid SQL identifier")
    return "`" + str(name).replace("`", "``") + "`"

def table_count(table):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM " + qi(table))
        return int(cursor.fetchone()[0])

def rows(sql, params=None):
    with connection.cursor() as cursor:
        cursor.execute(sql, params or [])
        names = [col[0] for col in cursor.description] if cursor.description else []
        return [dict(zip(names, row)) for row in cursor.fetchall()]

def unavailable(field):
    return Response({"detail": "EDA endpoint requires a confirmed schema column.", "missing_column": field},
                    status=status.HTTP_400_BAD_REQUEST)

class EDASummaryAPIView(APIView):
    def get(self, request):
        result = {"batting_records": table_count(CFG["bat_table"]),
                  "bowling_records": table_count(CFG["bowl_table"])}
        if CFG["meta_table"] in CFG:
            try:
                result["match_metadata_records"] = table_count(CFG["meta_table"])
            except Exception:
                result["match_metadata_records"] = None
        if CFG["runs"]:
            result["total_runs"] = rows("SELECT COALESCE(SUM(" + qi(CFG["runs"]) + "),0) AS total_runs FROM " + qi(CFG["bat_table"]))[0]["total_runs"]
        if CFG["wickets"]:
            result["total_wickets"] = rows("SELECT COALESCE(SUM(" + qi(CFG["wickets"]) + "),0) AS total_wickets FROM " + qi(CFG["bowl_table"]))[0]["total_wickets"]
        return Response(result)

class EDABattingAPIView(APIView):
    def get(self, request):
        c = CFG
        required = ["player", "runs"]
        missing = [x for x in required if not c.get(x)]
        if missing:
            return unavailable(", ".join(missing))
        select = [qi(c["player"]) + " AS player_name", "COUNT(*) AS innings", "SUM(" + qi(c["runs"]) + ") AS runs"]
        if c["balls"]: select.append("SUM(" + qi(c["balls"]) + ") AS balls_faced")
        if c["fours"]: select.append("SUM(" + qi(c["fours"]) + ") AS fours")
        if c["sixes"]: select.append("SUM(" + qi(c["sixes"]) + ") AS sixes")
        sql = "SELECT " + ", ".join(select) + " FROM " + qi(c["bat_table"]) + " WHERE " + qi(c["player"]) + " IS NOT NULL GROUP BY " + qi(c["player"]) + " ORDER BY runs DESC"
        return Response(rows(sql))

class EDABowlingAPIView(APIView):
    def get(self, request):
        c = CFG
        if not c["player"] or not c["wickets"] or not c["runs_conceded"]:
            return unavailable("player_name, wickets, runs_conceded")
        select = [qi(c["player"]) + " AS player_name", "COUNT(*) AS bowling_records",
                  "SUM(" + qi(c["wickets"]) + ") AS wickets",
                  "SUM(" + qi(c["runs_conceded"]) + ") AS runs_conceded"]
        if c["overs"]: select.append("SUM(" + qi(c["overs"]) + ") AS overs")
        sql = "SELECT " + ", ".join(select) + " FROM " + qi(c["bowl_table"]) + " WHERE " + qi(c["player"]) + " IS NOT NULL GROUP BY " + qi(c["player"]) + " ORDER BY wickets DESC, runs_conceded ASC"
        return Response(rows(sql))

class EDASeasonAPIView(APIView):
    def get(self, request):
        c = CFG
        if not c["season"] or not c["meta_match"]:
            return unavailable("season and match_id in match metadata")
        sql = "SELECT " + qi(c["season"]) + " AS season, COUNT(*) AS matches FROM " + qi(c["meta_table"]) + " GROUP BY " + qi(c["season"]) + " ORDER BY " + qi(c["season"])
        return Response(rows(sql))

class EDAVenueAPIView(APIView):
    def get(self, request):
        c = CFG
        if not c["venue"]:
            return unavailable("venue in match metadata")
        sql = "SELECT " + qi(c["venue"]) + " AS venue, COUNT(*) AS matches FROM " + qi(c["meta_table"]) + " WHERE " + qi(c["venue"]) + " IS NOT NULL GROUP BY " + qi(c["venue"]) + " ORDER BY matches DESC"
        return Response(rows(sql))

class EDAOppositionAPIView(APIView):
    def get(self, request):
        c = CFG
        if not c["opposition"]:
            return unavailable("opposition in match metadata")
        sql = "SELECT " + qi(c["opposition"]) + " AS opposition, COUNT(*) AS matches FROM " + qi(c["meta_table"]) + " WHERE " + qi(c["opposition"]) + " IS NOT NULL GROUP BY " + qi(c["opposition"]) + " ORDER BY matches DESC"
        return Response(rows(sql))

class EDARecentFormAPIView(APIView):
    def get(self, request):
        c = CFG
        player_name = (request.query_params.get("player_name") or "").strip()
        if not player_name:
            return Response({"detail": "player_name query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not c["player"] or not c["bat_match"]:
            return unavailable("player_name and match_id in batting table")
        # Stable sequence uses match_id unless a confirmed date column can be joined.
        sql = "SELECT * FROM " + qi(c["bat_table"]) + " WHERE " + qi(c["player"]) + " = %s ORDER BY " + qi(c["bat_match"]) + " DESC LIMIT 5"
        return Response(rows(sql, [player_name]))
