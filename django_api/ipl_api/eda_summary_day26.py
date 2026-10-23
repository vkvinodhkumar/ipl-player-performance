from django.http import JsonResponse
from django.db import connection, DatabaseError

def eda_summary_day26(request):
    """Return basic record counts for the dashboard; tolerate absent staging tables."""
    table_candidates = {
        "players": ("stg_ipl_batting_player_match", "player_name"),
        "matches": ("stg_ipl_match_metadata", None),
        "batting_records": ("stg_ipl_batting_player_match", None),
        "bowling_records": ("stg_ipl_bowling_player_match", None),
    }
    result = {"players": 0, "matches": 0, "batting_records": 0, "bowling_records": 0}
    errors = []
    with connection.cursor() as cursor:
        for key, (table, column) in table_candidates.items():
            try:
                if column:
                    cursor.execute(f"SELECT COUNT(DISTINCT `{column}`) FROM `{table}`")
                else:
                    cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
                row = cursor.fetchone()
                result[key] = int(row[0] or 0)
            except DatabaseError:
                errors.append(key)
    if errors:
        result["warning"] = "Some counts could not be loaded; verify MySQL staging tables: " + ", ".join(errors)
    return JsonResponse(result)
