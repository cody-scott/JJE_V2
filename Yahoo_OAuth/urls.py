from django.conf.urls import url, include
from . import views

from Yahoo_OAuth.api import views as api_views

urlpatterns = [
    url(r'^$', views.OAuthStart.as_view(), name='oauth_start'),
    url(r'^callback', views.OAuthCallback.as_view(), name="oauth_callback"),
    url(r'^refresh$', views.OAuthRefresh.as_view(), name="oauth_refresh")
]


urlpatterns += [
    url(r'api/getstandings', api_views.get_standings, name="get_standings"),
    url(r'api/getuserteams', api_views.get_user_team, name="get_user_teams"),
    url(r'api/getteams', api_views.get_teams, name="get_teams"),
]


