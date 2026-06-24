from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from shop.views import checkout
urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('', include('shop.urls')),        # ← обычные HTML-страницы (главная, об авторе и т.д.)
    path('api/', include('shop.api_urls')), # ← API
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
