from django.shortcuts import render

def dashboard_day25(request):
    """Render the IPL analytics dashboard shell."""
    return render(request, "ipl_api/dashboard_day25.html")
