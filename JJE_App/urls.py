from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

admin.site.site_title = "JJE Admin"
admin.site.site_header = "JJE Admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'accounts/', include('allauth.urls')),

    url(r'^', include('JJE_Main.urls'), name='main'),
    url(r'oauth/', include('Yahoo_OAuth.urls'), name='Yahoo_OAuth'),
    url(r'standings/', include('JJE_Standings.urls'), name='JJE_Standings'),

    url(r'^api-auth/', include('rest_framework.urls')),
]
