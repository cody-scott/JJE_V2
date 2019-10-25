from django.conf.urls import url, include
from JJE_Main import views
from JJE_Main.api import views as main_api
from rest_framework.routers import DefaultRouter, SimpleRouter
router = SimpleRouter()

router.register(r'guid', main_api.YahooTeamGUIDViewSetCurrentWeek, 'guid_api')
router.register(r'teams', main_api.YahooTeamViewSet, 'teams_api')

urlpatterns = [
    url(r'api/', include(router.urls), name='main_api')
]

urlpatterns += [
    url(r'^$', views.IndexView.as_view(), name='index')
]
