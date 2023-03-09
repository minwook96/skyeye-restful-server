from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register('site', SiteViewSet)
router.register('site_setting', SiteSettingsConfigViewSet)

urlpatterns = router.urls
