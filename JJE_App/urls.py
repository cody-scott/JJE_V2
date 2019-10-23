from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

admin.site.site_title = "JJE Admin"
admin.site.site_header = "JJE Admin"

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework.routers import DefaultRouter, SimpleRouter
router = DefaultRouter()

from JJE_Main.urls import router as main_router
router.registry.extend(main_router.registry)

from JJE_Standings.urls import router as standings_router
router.registry.extend(standings_router.registry)

#
# from JJE_Waivers.urls import router as waivers_router
# router.registry.extend(waivers_router.registry)

# from Yahoo_OAuth.urls import router as yahoo_oauth_router
# router.registry.extend(yahoo_oauth_router.registry)

urlpatterns = [url(r'api/', include(router.urls)),]


urlpatterns += [
    path('admin/', admin.site.urls),
    url(r'accounts/', include('allauth.urls')),

    url(r'^', include('JJE_Main.urls'), name='main'),
    url(r'^oauth/', include('Yahoo_OAuth.urls'), name='Yahoo_OAuth'),
    url(r'^standings/', include('JJE_Standings.urls'), name='JJE_Standings'),
    url(r'^waivers/', include('JJE_Waivers.urls'), name='JJE_Waivers'),

    url(r'^api-auth/', include('rest_framework.urls')),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


