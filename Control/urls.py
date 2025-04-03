from django.urls import path
from .views import login_view, dashboard_view, charts_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('charts/', charts_view, name='charts'),
]
