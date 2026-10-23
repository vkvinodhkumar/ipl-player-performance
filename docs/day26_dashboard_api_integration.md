# Day 26 — Dashboard Route Integration

## Generated files
- `django_api/ipl_api/dashboard_views_day26.py`
- `django_api/ipl_api/day26_dashboard_url_patch.txt`

## Automated checks
- View syntax: passed.
- `manage.py check` return code: 0.
- Day 21 regression test return code: 0.

## Manual integration still required
1. Merge the URL import and dashboard path into the existing `urls.py`.
2. Run `python manage.py check`.
3. Run `python manage.py runserver`.
4. Open `http://127.0.0.1:8000/dashboard/`.
5. Click Refresh summary and inspect the browser result for `/api/eda/summary/`.
6. Update metric mappings only after observing the actual JSON response.

Automated checks do not prove the route was merged, the template renders in a browser, or the API call succeeds.
