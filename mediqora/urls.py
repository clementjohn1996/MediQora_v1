from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from Control.views import dashboard_view 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='control/login.html'), name='login'),
    path('control/', include('Control.urls')),
    path('enquiry/', include('EnquiryManager.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', dashboard_view, name='home'),  
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)