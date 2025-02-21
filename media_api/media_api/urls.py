from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('fileprocessor.urls')),  # This includes 'upload/' under 'api/'
]
