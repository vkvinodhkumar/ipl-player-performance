# Day 27 — Dashboard Player Search and Analytics Foundation

- Generated: 2026-10-23T16:00:30
- Repository: `D:\Git\Personal\ipl-player-performance`

## Files updated
- `django_api\ipl_api\templates\ipl_api\dashboard_day25.html`
- `django_api\ipl_api\static\ipl_api\css\dashboard_day25.css`
- `django_api\ipl_api\static\ipl_api\js\dashboard_day25.js`

## Checks
- `python manage.py check` return code: **0**
- URL resolver command return code: **0**

## Behavior added
- Summary API request runs automatically on dashboard load and on refresh.
- Player search calls `/api/players/?search=<query>&page=1&page_size=20`.
- Handles common JSON list/`results`/`players`/`data` response shapes.
- Escapes returned values before rendering HTML.
- Displays actionable errors for failed requests or unknown response shapes.

## Important limitations
- A successful Django system check does not prove the summary or player endpoint works.
- Player search depends on the existing API actually implementing the `search` query parameter.
- Batting/bowling chart endpoints and prediction endpoints were not invented or silently registered here.
- Verify in a browser at `/api/dashboard/`; check `/api/eda/summary/` and `/api/players/?search=virat` directly.

## Top-level URL resolver output
```text
12 objects imported automatically (use -v 2 for details).


api/
admin/
--- API URLS ---
api/
api/api/
api/admin/
```
