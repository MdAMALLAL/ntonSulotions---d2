
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.conf.urls import handler400, handler403, handler404, handler500
from django.conf import settings
from django.contrib import admin
from . import views

# urlpatterns = [path('?admin/', admin.site.urls), ]
urlpatterns = i18n_patterns(
    path("csv", views.csv_view, name="csv"),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', views.HomePage.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("ticket/", include("solutions.urls", namespace="solutions")),
    path('client/', include('clients.urls',namespace='clients'))
)   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)


handler400 = 'ntonSulotions.views.handler400'
handler403 = 'ntonSulotions.views.handler403'
handler404 = 'ntonSulotions.views.handler404'
handler500 = 'ntonSulotions.views.handler500'
