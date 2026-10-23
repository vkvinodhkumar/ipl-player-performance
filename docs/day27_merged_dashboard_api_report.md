# Day 27 — Merged Dashboard and DRF API Repair

- Generated: 2026-10-23T21:43:42
- Repository: `D:\Git\Personal\ipl-player-performance`
- Settings file: `django_api\config\settings.py`
- Settings backup: `django_api\config\settings.py.day27_merged_backup_20261023_214337`

## Dashboard files updated
- `django_api\ipl_api\templates\ipl_api\dashboard_day25.html`
- `django_api\ipl_api\static\ipl_api\css\dashboard_day25.css`
- `django_api\ipl_api\static\ipl_api\js\dashboard_day25.js`

## Checks
- Django system check return code: **0**
- Endpoint probe command return code: **0**
- DRF default renderer configured as JSONRenderer only to avoid the missing browsable API HTML template.

## Endpoint probe output
```text
12 objects imported automatically (use -v 2 for details).

URL: /api/eda/summary/
STATUS: 400
CONTENT_TYPE: text/plain; charset=utf-8
BODY_PREVIEW: DisallowedHost at /api/eda/summary/
Invalid HTTP_HOST header: 'testserver'. You may need to add 'testserver' to ALLOWED_HOSTS.

Request Method: GET
Request URL: http://testserver/api/eda/summary/
Django Version: 6.0.9
Python Executable: c:\Users\Vinod\anaconda3\envs\ipl-player-performance\python.exe
Python Version: 3.12.14
Python Path: ['D:\\Git\\Personal\\ipl-player-performance\\django_api', 'c:\\Users\\Vinod\\anaconda3\\envs\\ipl-player-performance\\python312.zip', 'c:\\Users\\Vinod\\anaconda3\\envs\\ipl-player-performance\\DLLs', 'c:\\Users\\Vinod\\anaconda3\\envs\\ipl-player-performance\\Lib', 'c:\\Users\\Vinod\\anaconda3\\envs\\ipl-player-performance', 'c:\\Users\\Vinod\\anaconda3\\envs\\ipl-player-performance\\Lib\\site-packages', 'c:\\Users\\Vinod\\anaconda3\\envs\\ipl-player-performance\\Lib\\site-packages\\win32', 'c:\\Users\\Vinod\\anaconda3\\envs\\ipl-player-performance\\Lib\\site-packages\\win32\\lib', 'c:\\Users\\Vinod\\anaconda3\\envs\\ipl-player-performance\\Lib\\site-packages\\pythonwin']
Server time: Fri, 23 Oct 2026 16:13:41 +0000
Installed Applications:
['django.contrib.admin',
 'django.contrib.auth',
 'django.contrib.contenttypes',
 'django.contrib.sessions',
 '
---
URL: /api/players/
STATUS: 400
CONTENT_TYPE: text/plain; charset=utf-8
BODY_PREVIEW: DisallowedHost at /api/players/
Invalid HTTP_HOST header: 'testserver'. You may need to add 'testserver' to ALLOWED_HOSTS.

Request Method: GET
Request URL: http://testserver/api/players/
Django Version: 6.0.9
Python Executable: c:\Users\Vinod\anaconda3\envs\ipl-player-performance\python.exe
Python Version: 3.12.14
Python Path: ['D:\\Git\\Personal\\ipl-player-performance\\django_api', 'c:\\Users\\Vinod\\anaconda3\\envs\\ipl-player-performance\\python312.zip', 'c:\\Users\\Vinod\\anaconda3\\envs\\ipl-player-performance\\DLLs', 'c:\\Users\\Vinod\\anaconda3\\envs\\ipl-player-performance\\Lib', 'c:\\Users\\Vinod\\anaconda3\\envs\\ipl-player-performance', 'c:\\Users\\Vinod\\anaconda3\\envs\\ipl-player-performance\\Lib\\site-packages', 'c:\\Users\\Vinod\\anaconda3\\envs\\ipl-player-performance\\Lib\\site-packages\\win32', 'c:\\Users\\Vinod\\anaconda3\\envs\\ipl-player-performance\\Lib\\site-packages\\win32\\lib', 'c:\\Users\\Vinod\\anaconda3\\envs\\ipl-player-performance\\Lib\\site-packages\\pythonwin']
Server time: Fri, 23 Oct 2026 16:13:42 +0000
Installed Applications:
['django.contrib.admin',
 'django.contrib.auth',
 'django.contrib.contenttypes',
 'django.contrib.sessions',
 'django.c
---
URL: /api/players/?search=virat&page=1&page_size=20
STATUS: 400
CONTENT_TYPE: text/plain; charset=utf-8
BODY_PREVIEW: DisallowedHost at /api/players/
Invalid HTTP_HOST header: 'testserver'. You may need to add 'testserver' to ALLOWED_HOSTS.

Request Method: GET
Request URL: http://testserver/api/players/?search=virat&page=1&page_size=20
Django Version: 6.0.9
Python Executable: c:\Users\Vinod\anaconda3\envs\ipl-player-performance\python.exe
Python Version: 3.12.14
Python Path: ['D:\\Git\\Personal\\ipl-player-performance\\django_api', 'c:\\Users\\Vinod\\anaconda3\\envs\\ipl-player-performance\\python312.zip', 'c:\\Users\\Vinod\\anaconda3\\envs\\ipl-player-performance\\DLLs', 'c:\\Users\\Vinod\\anaconda3\\envs\\ipl-player-performance\\Lib', 'c:\\Users\\Vinod\\anaconda3\\envs\\ipl-player-performance', 'c:\\Users\\Vinod\\anaconda3\\envs\\ipl-player-performance\\Lib\\site-packages', 'c:\\Users\\Vinod\\anaconda3\\envs\\ipl-player-performance\\Lib\\site-packages\\win32', 'c:\\Users\\Vinod\\anaconda3\\envs\\ipl-player-performance\\Lib\\site-packages\\win32\\lib', 'c:\\Users\\Vinod\\anaconda3\\envs\\ipl-player-performance\\Lib\\site-packages\\pythonwin']
Server time: Fri, 23 Oct 2026 16:13:42 +0000
Installed Applications:
['django.contrib.admin',
 'django.contrib.auth',
 'django.contrib.contenttypes',
 'dja
---
```

## Verification notes
- A 200 JSON response confirms JSON API access, not necessarily search filtering.
- Compare `/api/players/` and `?search=virat` results to verify search behavior.
- Summary card counts are populated from the API response, not hardcoded.
- Browser verification remains necessary at `http://127.0.0.1:8000/api/dashboard/`.
