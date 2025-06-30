from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Inclua as rotas da sua API
    path('silk/', include('silk.urls', namespace='silk')),
]