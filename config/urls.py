from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [

    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("store/" , include("jusciogrybai.store.urls")),
    path(settings.ADMIN_URL, admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

