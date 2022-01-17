from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from shargain.notifications.urls import router as notifications_router
from shargain.offers.urls import router as offers_router

router = DefaultRouter()

router.registry.extend(offers_router.registry)
router.registry.extend(notifications_router.registry)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
