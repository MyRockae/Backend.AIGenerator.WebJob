from django.urls import path, include
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/generator/', include('apps.generator.urls')),  # Include the accounts app URLs
    path('', include('apps.utility.urls')),
    # OpenAPI schema:
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Redoc:
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
        # Catch-all for undefined routes, redirect to home page
    path('<path:slug>/', lambda request, slug: redirect('home')),  
]
