from django.shortcuts import render

# Create your views here.

def dashboard(request):
    """
    Render the dashboard page.
    """
    return render(request, 'tasks/dashboard.html', context={})