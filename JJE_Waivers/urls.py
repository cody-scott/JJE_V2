from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^waiver_claim/new/$',
        views.WaiverClaimCreate.as_view(),
        name="waiver_claim-add"),
    url(r'^waiver_claim/overclaim=(?P<pk>[0-9]+)$',
        views.OverclaimCreate.as_view(),
        name="waiver_claim-overclaim"),
    url(r'^waiver_claim/cancel=(?P<pk>[0-9]+)$',
        views.CancelClaimView.as_view(),
        name="waiver_claim-cancel"),
]
