from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),

    # busines logic
    path('', include('product.urls')),
    
    # auth and user data
    path('', include('user_profile.urls')),
    path('oauth/google/', include('google_login_server_flow.urls')),

    # schema 
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
