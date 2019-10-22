from django.conf.urls import url, include
from . import views


from rest_framework.routers import DefaultRouter

from JJE_Standings.api import views as standings_api

router = DefaultRouter()
# router.register(r'all_standings', standings_api.StandingsViewSet)

router.register(r'all_standings', standings_api.AllStandingsViewSet, 'all_standings')
router.register(r'current_standings', standings_api.CurrentStandingsViewSet, 'current_standings')
router.register(r'current_guid', standings_api.YahooTeamGUIDViewSetCurrentWeek, 'current_guid')
router.register(r'guid', standings_api.YahooGUIDViewSet, 'guid')
router.register(r'teams', standings_api.YahooTeamGUIDViewSet, 'teams')

# router.register(r'ranks', standings_api.YahooStandingTmp)

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='standings_index'),
    url(r'^api/', include(router.urls)),
]
