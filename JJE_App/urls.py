"""JJE_App1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include, url

admin.site.site_title = "JJE Admin"
admin.site.site_header = "JJE Admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'accounts/', include('allauth.urls')),

    url(r'', include('JJE_Main.urls'), name='main'),
    url(r'oauth/', include('Yahoo_Authentication.urls'), name='Yahoo_Authentication'),
    url(r'standings/', include('JJE_Standings.urls'), name='JJE_Standings'),
]
