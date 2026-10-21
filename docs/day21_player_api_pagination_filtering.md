# Day 21 — Player API Pagination and Filtering

- Generated: 2026-10-21T23:42:47
- Repository: `D:\Git\Personal\ipl-player-performance`
- Helper: `D:\Git\Personal\ipl-player-performance\django_api\ipl_api\pagination_utils.py`
- Tests: `D:\Git\Personal\ipl-player-performance\django_api\ipl_api\tests\test_pagination_utils_day21.py`
- Django check return code: **0**
- Pagination test return code: **0**

## Django check output

```text
System check identified no issues (0 silenced).\n
```

## Pagination test output

```text
Found 6 test(s).\nSkipping setup of unused database(s): default.\nSystem check identified no issues (0 silenced).\n\ntest_defaults (ipl_api.tests.test_pagination_utils_day21.PaginationHelperTests.test_defaults) ... ok\ntest_paginates_records (ipl_api.tests.test_pagination_utils_day21.PaginationHelperTests.test_paginates_records) ... ok\ntest_rejects_non_integer (ipl_api.tests.test_pagination_utils_day21.PaginationHelperTests.test_rejects_non_integer) ... ok\ntest_rejects_oversized_page_size (ipl_api.tests.test_pagination_utils_day21.PaginationHelperTests.test_rejects_oversized_page_size) ... ok\ntest_rejects_zero_page (ipl_api.tests.test_pagination_utils_day21.PaginationHelperTests.test_rejects_zero_page) ... ok\ntest_valid_values (ipl_api.tests.test_pagination_utils_day21.PaginationHelperTests.test_valid_values) ... ok\n\n----------------------------------------------------------------------\nRan 6 tests in 0.001s\n\nOK
```

## Integration status

This notebook creates and tests a reusable helper. It does not rewrite the existing Player List view. Integrate the helper into the existing API using the actual SQL query and player-name column. For large datasets, use parameterized SQL LIMIT/OFFSET.

## API contract

- `GET /api/players/?page=1&page_size=20`
- `GET /api/players/?search=virat`
- `page >= 1`; `1 <= page_size <= 100`
- Suggested response keys: `count`, `page`, `page_size`, `total_pages`, `results`
