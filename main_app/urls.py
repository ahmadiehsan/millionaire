from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('apps.core.urls')),
    path('game/', include('apps.game.urls')),
    path('user/', include('apps.user.urls')),
    path('admin/', admin.site.urls),
]
