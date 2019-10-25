from django.conf.urls import url, include
from . import views

from JJE_Standings.api import views as standings_api
from rest_framework.routers import DefaultRouter, SimpleRouter
router = SimpleRouter()

router.register(r'current_standings', standings_api.CurrentStandingsViewSet, 'current_standings')
router.register(r'all_standings', standings_api.AllStandingsViewSet, 'all_standings')

urlpatterns = [url(r'api/', include(router.urls))]

urlpatterns += [
    url(r'^$', views.IndexView.as_view(), name='standings_index'),
]
