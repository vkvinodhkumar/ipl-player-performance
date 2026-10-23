# Day 26 — Dashboard Route Integration

## Generated files
- `django_api/ipl_api/dashboard_views_day26.py`
- `django_api/config/urls.py` (updated only if needed)
- `django_api/ipl_api/urls.py` (dashboard and EDA summary routes merged only if needed)

## Automated checks
- `manage.py check` return code: 0.
- URL resolver return code: 0.
- Day 21 regression test return code: 0.

## Manual integration still required
1. Run `python manage.py runserver` from `django_api`.
2. Open `http://127.0.0.1:8000/api/dashboard/`.
3. Confirm the Day 26 dashboard shell appears.
4. Test the summary request at `http://127.0.0.1:8000/api/eda/summary/`.
5. Review the generated detailed report at `docs/day26_api_dashboard_repair_report.md`.

Automated checks do not prove database queries, model inference, or browser interactions succeed.
