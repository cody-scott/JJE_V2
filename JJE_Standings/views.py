from django.views.generic import View, TemplateView
from django.http import HttpResponse

from JJE_Standings.utils.yahoo_data import build_team_data, update_standings, test_standings
from JJE_Standings.utils import \
    get_standings_json, email_standings, check_if_update_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse


class IndexView(TemplateView):
    """
    This is for rendering out the standings graph
    Some work to be done here
    """
    template_name = "JJE_Standings/standings.html"

    # def get(self, request):
    #     return HttpResponse("")


class UpdateStandings(View):
    def get(self, request):
        # if check_if_update_required():
        update_standings(request)
        email_standings()
        return HttpResponse(
            "<pre>{}</pre>".format(get_standings_json()))


# class CreateTeams(View):
#     def get(self, request):
#         if build_team_data(request):
#             return HttpResponse("Done")
#         else:
#             return HttpResponse("Error")


@method_decorator(login_required, name='dispatch')
class TestToken(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect(reverse('index'))

        results, status_code = test_standings(request)
        # email_standings()
        return HttpResponse(
            "<h1>Status: {}</h1><br><a>{}</a>".format(status_code, results.content))


@method_decorator(login_required, name='dispatch')
class GenerateStandingsToken(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect(reverse('index'))


