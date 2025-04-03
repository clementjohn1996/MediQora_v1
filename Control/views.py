from django.shortcuts import render

def login_view(request):
    return render(request, 'Control/login.html')

def dashboard_view(request):
    return render(request, 'Control/dashboard.html')

def charts_view(request):
    return render(request, 'Control/charts.html')
