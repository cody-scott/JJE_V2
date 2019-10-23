from django.conf.urls import url, include
from . import views

from JJE_Standings.api import views as standings_api
from rest_framework.routers import DefaultRouter, SimpleRouter
router = SimpleRouter()

# router.register(r'all_standings', standings_api.AllStandingsViewSet, base_name='all_standings')
# router.register(r'standings_guid', standings_api.YahooGUIDViewSet, base_name='standings_guid')
# router.register(r'current_standings', standings_api.CurrentStandingsViewSet, base_name='current_standings')
# router.register(r'current_guid', standings_api.YahooTeamGUIDViewSetCurrentWeek, base_name='current_guid')
# router.register(r'standings_teams', standings_api.YahooTeamGUIDViewSet, base_name='standings_teams')

router.register(r'current_standings', standings_api.CurrentStandingsViewSet, 'current_standings')
router.register(r'all_standings', standings_api.AllStandingsViewSet, 'all_standings')


urlpatterns = [url(r'api/', include(router.urls))]

urlpatterns += [
    url(r'^$', views.IndexView.as_view(), name='standings_index'),
]
