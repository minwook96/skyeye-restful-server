"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token
from .views import *
from django.conf.urls import handler400, handler403, handler404, handler500

schema_view = get_schema_view(
    openapi.Info(
        title="server-restful-server",
        default_version='v1.0.0',
        description="server-restful API 문서",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="skysys@skysys.co.kr"),  # 부가 정보
        # license=openapi.License(name="mit"),  # 부가 정보
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("api-auth/", include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token),
    # 이 아랫 부분은 우리가 사용하는 app들의 URL들을 넣습니다.
    # path('', homescreen_view, name='home'),
    path("", include("sse.urls")),
    path("", include("mission_device.urls")),
    path("", include("winch.urls")),
    path("", include("fire_detection.urls")),
    path("", include("skyeye.urls")),
    path("", include("helikite.urls")),
    path("", include("accounts.urls")),

] # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r"^swagger/$", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r"^redoc/$", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
]

# handler400 = 'server.views.bad_request'
# handler403 = defaults.permission_denied
# handler404 = 'server.views.page_not_found'
# handler500 = defaults.server_error