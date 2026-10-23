from django.db import connection
from django.http import JsonResponse
from django.views.decorators.http import require_GET

@require_GET
def player_suggestions(request):
    q = (request.GET.get("q") or "").strip()
    if not q:
        return JsonResponse({"results": []})
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT player_name FROM ("
                "SELECT player_name FROM stg_ipl_batting_player_match WHERE player_name IS NOT NULL AND TRIM(player_name) <> '' "
                "UNION SELECT player_name FROM stg_ipl_bowling_player_match WHERE player_name IS NOT NULL AND TRIM(player_name) <> ''"
                ") p WHERE LOWER(player_name) LIKE LOWER(%s) GROUP BY player_name ORDER BY player_name LIMIT 20",
                [f"%{q}%"])
            rows = [{"player_name": r[0]} for r in cursor.fetchall()]
        return JsonResponse({"results": rows})
    except Exception as exc:
        return JsonResponse({"detail": "Suggestions unavailable", "error": str(exc)}, status=503)
