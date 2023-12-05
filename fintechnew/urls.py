
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('finweb.urls')),
    path('Payments/', include('Payments.urls')),
    path('api/', include('api_integration.urls')),
]

