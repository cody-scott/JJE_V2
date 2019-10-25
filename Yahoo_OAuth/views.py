from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from django.contrib.sites.models import Site

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse

import django.dispatch

# Create your views here.
from Yahoo_OAuth.utils.oauth_flow import \
    start_oauth, callback_oauth, refresh_current_token

oauth_complete_signal = django.dispatch.Signal(providing_args=["request"])
oauth_refresh_signal = django.dispatch.Signal(providing_args=["request"])


@method_decorator(login_required, name='dispatch')
class OAuthStart(View):
    def get(self, request):
        return start_oauth(request)


@method_decorator(login_required, name='dispatch')
class OAuthCallback(View):
    def get(self, request):
        callback_oauth(request)
        oauth_complete_signal.send(sender=self.__class__, request=request)
        return redirect(reverse("waivers_index"))


@method_decorator(login_required, name='dispatch')
class OAuthRefresh(View):
    def get(self, request):
        refresh_current_token(request)
        oauth_refresh_signal.send(sender=self.__class__, request=request)
        return redirect(reverse("waivers_index"))
