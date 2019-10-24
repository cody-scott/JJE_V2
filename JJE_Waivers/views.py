from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib import messages


from JJE_Waivers.models import WaiverClaim
from JJE_Waivers.utils import show_oauth_link
from JJE_Waivers.utils import api_calls


from JJE_Waivers.utils import waiver_functions


from django.http import HttpResponse
from django.views import View


from django.http import JsonResponse
from JJE_Main.models import YahooTeam


# class MyView(View):
#     def get(self, request, *args, **kwargs):
#         teams = api_calls.get_users_teams_waivers(request)
#         overclaims = api_calls.get_overclaim_teams(request, teams)
#
#         return JsonResponse({'a': 1})
#         # return JsonResponse(yahoo_team.get_user_teams(request).json(), safe=False)


class IndexView(ListView):
    template_name = "JJE_Waivers/waivers_index.html"

    def get_queryset(self):
        now = timezone.now() - timedelta(days=1)
        claims = WaiverClaim.objects \
            .filter(cancelled=False) \
            .filter(overclaimed=False) \
            .filter(claim_start__gt=now) \
            .order_by('claim_start')
        return claims

    def get_context_data(self, **kwargs):
        oauth_display = show_oauth_link(self.request)

        context = super(IndexView, self).get_context_data(**kwargs)

        user_teams = []
        overclaim_teams = []
        if (not self.request.user.is_anonymous) and (oauth_display is False):
            # query for users teams via api using GUID
            user_teams = api_calls.get_users_teams_waivers_request(self.request)

            # these ids are the teams that the user CAN overclaim
            overclaim_teams = api_calls.get_overclaim_teams(self.request, user_teams)

        context['user_team_ids'] = [val['id'] for val in user_teams]
        context['overclaim_ids'] = overclaim_teams
        context['show_oauth'] = oauth_display
        return context


@method_decorator(login_required, name='dispatch')
class WaiverClaimCreate(CreateView):
    model = WaiverClaim
    template_name_suffix = "_new"
    fields = [
        "yahoo_team",
        "add_player", "add_LW", "add_C", "add_RW",
        "add_D", "add_G", "add_Util", "add_IR",
        "drop_player", "drop_LW", "drop_C", "drop_RW",
        "drop_D", "drop_G", "drop_Util", "drop_IR",
        "claim_message",
    ]

    def get(self, request, *args, **kwargs):
        if self.request.user.usertoken_set.first() is None:
            return redirect(reverse('oauth_start'))
        return super(WaiverClaimCreate, self).get(request, *args, **kwargs)

    def get_form(self, form_class=None):
        frm = super(WaiverClaimCreate, self).get_form(form_class)

        ids = api_calls.get_users_teams_waivers_request(self.request)
        usr_teams = [v.get('id') for v in ids]

        frm.fields['yahoo_team'].queryset = YahooTeam.objects.filter(
            id__in=usr_teams
        )

        return frm

    def get_initial(self):
        ids = api_calls.get_users_teams_waivers_request(self.request)
        usr_teams = {'yahoo_team': v.get('id') for v in ids}

        return usr_teams

    def form_valid(self, form):
        valid_form = super(WaiverClaimCreate, self).form_valid(form)
        messages.add_message(self.request, messages.INFO,
                             "Claim Successful")
        # email_functions.claim_email(self.object, "New Claim", self.request)
        return valid_form


@method_decorator(login_required, name='dispatch')
class OverclaimCreate(CreateView):
    model = WaiverClaim
    template_name_suffix = "_overclaim"
    fields = [
        "yahoo_team",
        "drop_player", "drop_LW", "drop_C", "drop_RW",
        "drop_D", "drop_G", "drop_Util", "drop_IR",
        "claim_message",
    ]

    def get(self, request, *args, **kwargs):
        try:
            if not waiver_functions.check_if_standings():
                raise AssertionError

            wc_id = self.kwargs.get("pk")
            player = WaiverClaim.objects.get(id=wc_id)

            if not player.active_claim():
                messages.add_message(request, messages.WARNING,
                                     "Waiver claim is no longer active")
                assert player.active_claim()

            claim_team_standing = api_calls.get_claim_team_rank(self.request, player.yahoo_team.id)
            claimee_standings = api_calls.get_user_team_ranks(self.request)

            if len(claimee_standings) > 0:
                cts = claim_team_standing
                cee = max(claimee_standings)
                if cts >= cee:
                    messages.add_message(request, messages.WARNING,
                                         "Claim team is lower ranked then you")
                    raise AssertionError

            return super(OverclaimCreate, self).get(request, *args, **kwargs)
        except Exception as e:
            return e
            print(e)
            return redirect(reverse("waivers_index"))

    def get_initial(self):
        ids = api_calls.get_users_teams_waivers_request(self.request)
        usr_teams = {'yahoo_team': v.get('id') for v in ids}
        return usr_teams

    def get_form(self, form_class=None):
        frm = super(OverclaimCreate, self).get_form(form_class)
        wc_id = self.kwargs.get("pk")
        player = WaiverClaim.objects.get(id=wc_id)
        frm.fields['yahoo_team'].queryset = self.get_rank(self.request, player)
        return frm

    def get_context_data(self, **kwargs):
        context = super(OverclaimCreate, self).get_context_data(**kwargs)
        wc_id = self.kwargs.get("pk")
        player = WaiverClaim.objects.get(id=wc_id)
        context["add_name"] = player.add_player
        context["add_pos"] = player.get_position_add
        return context

    def form_valid(self, form):
        wc_id = self.kwargs.get("pk")
        player = WaiverClaim.objects.get(id=wc_id)
        player.overclaimed = True
        player.save()

        form.instance.claim_start = player.claim_start
        form.instance.add_player = player.add_player
        form.instance.add_LW = player.add_LW
        form.instance.add_C = player.add_C
        form.instance.add_RW = player.add_RW
        form.instance.add_D = player.add_D
        form.instance.add_G = player.add_G
        form.instance.add_Util = player.add_Util
        form.instance.add_IR = player.add_IR
        form.instance.over_claim_id = int(wc_id)
        valid_form = super(OverclaimCreate, self).form_valid(form)

        messages.add_message(self.request, messages.INFO,
                             "Overclaim Successful")

        # email_functions.claim_email(self.object, "Overclaim", self.request)

        return valid_form

    def get_rank(self, request, player):
        try:
            player = player
            rank = player.team.yahoostanding_set.filter(
                current_standings=True
            ).first().rank

            ranks = [
                team.team.id
                for team in YahooStanding.objects.filter(
                    current_standings=True).filter(rank__gte=rank).all()

            ]
            return YahooTeam.objects.filter(pk__in=ranks) \
                .filter(user=self.request.user.id)
        except:
            return YahooTeam.objects.filter(user=self.request.user.id) \
                .exclude(id=player.team.id)


@method_decorator(login_required, name='dispatch')
class CancelClaimView(DetailView):
    template_name = 'JJE_Waivers/waiverclaim_cancel.html'
    model = WaiverClaim

    def get(self, request, *a, **k):
        id = int(k.get("pk"))
        claim_obj = WaiverClaim.objects.filter(id=id).first()
        if claim_obj is None or not claim_obj.active_claim():
            return redirect(reverse("index"))

        if self.check_if_user_claim(request, id):
            return super(CancelClaimView, self).get(request, *a, **k)
        else:
            return redirect(reverse("index"))

    def check_if_user_claim(self, request, id):
        for team in [team for team in self.request.user.yahooteam_set.all()]:
            claims = [claim.id for claim in team.waiverclaim_set.all()]
            if id in claims:
                return True
        return False

    def post(self, request, *args, **kwargs):
        if request.user.yahooteam_set is None:
            return redirect(reverse('index'))

        claim_id = kwargs.get("pk")
        claim = get_object_or_404(WaiverClaim, id=claim_id)

        if claim.team.id not in [
            team.id for team in request.user.yahooteam_set.all()
        ]:
            return redirect(reverse('index'))

        claim.cancelled = True
        claim.save()
        messages.add_message(self.request, messages.INFO,
                             "Claim cancelled")
        email_functions.cancel_email(claim, request)
        return redirect(reverse('index'))
