from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'', views.IndexView.as_view(), name='standings_index'),
    # url(r'^update$', views.UpdateStandings.as_view(), name="update_standings"),
    # url(r'^maketeams$', views.CreateTeams.as_view(), name="create_teams"),
    # url(r'^testtoken$', views.TestToken.as_view(), name="test_token"),
]
