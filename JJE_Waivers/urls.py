from django.conf.urls import url, include
from . import views


# from JJE_Waivers.api import views as waivers_api
from rest_framework.routers import DefaultRouter, SimpleRouter
router = SimpleRouter()

#
# router.register(r'waivers_guid', waivers_api.YahooTeamGUIDViewSetCurrentWeek, base_name='waivers_guid')
#
#

urlpatterns = [
    url(r'api/', include(router.urls))
]

urlpatterns += [
    # url(r'^$', views.MyView.as_view(), name='index'),
    url(r'^$', views.IndexView.as_view(), name='waivers_index'),
    url(r'^new/',
        views.WaiverClaimCreate.as_view(),
        name="waiver_claim-add"),

    url(r'^overclaim=(?P<pk>[0-9]+)$',
        views.OverclaimCreate.as_view(),
        name="waiver_claim-overclaim"),
    url(r'^cancel=(?P<pk>[0-9]+)$',
        views.CancelClaimView.as_view(),
        name="waiver_claim-cancel"),
]

