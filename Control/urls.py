from django.urls import path
from .views import login_view, dashboard_view, charts_view, profile_view, settings_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('charts/', charts_view, name='charts'),
    path("ajax/profile/", profile_view, name="profile"),
    path("ajax/settings/", settings_view, name="settings"),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
