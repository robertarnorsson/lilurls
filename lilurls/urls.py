from django.contrib import admin
from django.urls import include, path, handler404, handler500
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", include("shortener.urls")),
    path("terms/", TemplateView.as_view(template_name="terms.html"), name="terms"),
    path("privacy/", TemplateView.as_view(template_name="privacy.html"), name="privacy"),
    path("robots.txt",TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots"),
    path('admin/', admin.site.urls),
]

handler500 = 'shortener.views.error_500'
handler404 = 'shortener.views.error_404'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()