from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.OAuthStart.as_view(), name='oauth_start'),
    url(r'^callback', views.OAuthCallback.as_view(), name="oauth_callback"),
    url(r'^refresh$', views.OAuthRefresh.as_view(), name="oauth_refresh")
]
