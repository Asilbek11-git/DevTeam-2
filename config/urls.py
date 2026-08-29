"""
Main URL Configuration for DevTeam SaaS.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    # Django Administration
    path('admin/', admin.site.urls),

    # OpenAPI 3.0 & Swagger UI documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # REST API v1 Endpoints
    path('api/v1/', include('apps.api.urls')),

    # Frontend Django Template Routes
    path('', include('apps.core.urls')),
    path('workspaces/', include('apps.workspaces.urls')),
    path('clients/', include('apps.workspaces.client_urls')),
    path('leads/', include('apps.workspaces.lead_urls')),
    path('services/', include('apps.billing.service_urls')),
    path('portfolio/', include('apps.accounts.portfolio_urls')),
    path('finance/', include('apps.billing.finance_urls')),
    path('projects/', include('apps.projects.urls')),
    path('boards/', include('apps.boards.urls')),
    path('tasks/', include('apps.tasks.urls')),
    path('sprints/', include('apps.sprints.urls')),
    path('billing/', include('apps.billing.urls')),
    path('auth/', include('apps.accounts.urls')),

]

handler400 = 'apps.core.views.custom_bad_request_view'
handler403 = 'apps.core.views.custom_permission_denied_view'
handler404 = 'apps.core.views.custom_page_not_found_view'
handler500 = 'apps.core.views.custom_server_error_view'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
