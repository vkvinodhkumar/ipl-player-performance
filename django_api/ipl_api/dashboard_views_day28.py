from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render

@ensure_csrf_cookie
def dashboard_day28(request):
    return render(request, 'ipl_api/dashboard_day28.html')
