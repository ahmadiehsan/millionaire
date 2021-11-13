from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('apps.core.urls')),
    path('exams/', include('apps.exam.urls')),
    path('users/', include('apps.user.urls')),
    path('admin/', admin.site.urls),
]
