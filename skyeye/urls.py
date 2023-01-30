from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register('site', SiteSerializer)
urlpatterns = router.urls
