from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib import messages

from JJE_Waivers.models import WaiverClaim

from JJE_Main.utils import jje_main_functions
from JJE_Standings.utils import jje_standings_functions

from JJE_Waivers.utils import jje_waiver_functions
from JJE_Waivers.utils import email_functions


class IndexView(ListView):
    template_name = "JJE_Waivers/waivers_index.html"

    def get_queryset(self):
        return jje_waiver_functions.get_active_claims()

    def get_context_data(self, **kwargs):
        oauth_display = jje_waiver_functions.show_oauth_link(self.request)

        context = super(IndexView, self).get_context_data(**kwargs)

        user_teams = []
        overclaim_teams = []
        if (not self.request.user.is_anonymous) and (oauth_display is False):
            # query for users teams via api using GUID
            guid = self.request.user.usertoken_set.first().user_guid
            user_teams = jje_main_functions.get_users_teams_ids(guid)
            # these ids are the teams that the user CAN overclaim
            overclaim_teams = jje_standings_functions.get_overclaim_teams(user_teams)

        context['user_team_ids'] = user_teams
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
        guid = self.request.user.usertoken_set.first().user_guid
        frm.fields['yahoo_team'].queryset = jje_main_functions.get_users_teams_qs(guid)
        return frm

    def get_initial(self):
        guid = self.request.user.usertoken_set.first().user_guid
        ids = jje_main_functions.get_users_teams_waivers(guid)
        if len(ids) == 1:
            return {'yahoo_team': v.get('id') for v in ids}
        else:
            return {'yahoo_team': None}

    def form_valid(self, form):
        valid_form = super(WaiverClaimCreate, self).form_valid(form)
        messages.add_message(self.request, messages.INFO,
                             "Claim Successful")
        email_functions.claim_email(self.object, "New Claim", self.request)
        return redirect(reverse('waivers_index'))


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
            if not jje_standings_functions.check_if_standings():
                raise AssertionError

            wc_id = self.kwargs.get("pk")
            player = WaiverClaim.objects.get(id=wc_id)
            # asserting the claim is still active
            if not player.active_claim():
                messages.add_message(request, messages.WARNING,
                                     "Waiver claim is no longer active")
                assert player.active_claim()

            # want to assert that the team holding the claim is in the overclaim list
            guid = self.request.user.usertoken_set.first().user_guid
            user_teams = jje_main_functions.get_users_teams_waivers(guid)
            team_ids = [t['id'] for t in user_teams]
            # these ids are the teams that the user CAN overclaim
            overclaim_teams = jje_standings_functions.get_overclaim_teams(team_ids)
            if not player.yahoo_team.id in overclaim_teams:
                messages.add_message(request, messages.WARNING,
                                     "Claim team is lower ranked then you")
                raise AssertionError

            return super(OverclaimCreate, self).get(request, *args, **kwargs)
        except Exception as e:
            return redirect(reverse("waivers_index"))

    def get_initial(self):
        guid = self.request.user.usertoken_set.first().user_guid
        ids = jje_main_functions.get_users_teams_waivers(guid)
        if len(ids) == 1:
            return {'yahoo_team': v.get('id') for v in ids}
        else:
            return {'yahoo_team': None}

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

        email_functions.claim_email(self.object, "Overclaim", self.request)
        return redirect(reverse('waivers_index'))

    def get_rank(self, request, player):
        # get the id of the claim team
        team_id = player.yahoo_team.id
        # get the overclaim ids for current claim holder that team
        overclaim_teams = jje_standings_functions.get_overclaim_teams([team_id])
        overclaim_teams.append(team_id)
        # exclude any teams that are in the overclaim list
        guid = self.request.user.usertoken_set.first().user_guid
        user_teams = jje_main_functions.get_users_teams_ids(guid)
        # filter list of team ids that can overclaim
        user_overclaim_teams = [x for x in user_teams if x not in overclaim_teams]
        team_qs = jje_main_functions.get_teams_qs(user_overclaim_teams)
        return team_qs


@method_decorator(login_required, name='dispatch')
class CancelClaimView(DetailView):
    template_name = 'JJE_Waivers/waiverclaim_cancel.html'
    model = WaiverClaim

    def get(self, request, *a, **k):
        id = int(k.get("pk"))
        claim_obj = WaiverClaim.objects.filter(id=id).first()
        if claim_obj is None or not claim_obj.active_claim():
            return redirect(reverse("waivers_index"))

        guid = self.request.user.usertoken_set.first().user_guid
        user_teams = jje_main_functions.get_users_teams_ids(guid)
        if not claim_obj.yahoo_team.id in user_teams:
            return redirect(reverse("waivers_index"))

        return super(CancelClaimView, self).get(request, *a, **k)

    def post(self, request, *args, **kwargs):
        claim_id = kwargs.get("pk")
        claim = get_object_or_404(WaiverClaim, id=claim_id)

        guid = self.request.user.usertoken_set.first().user_guid
        user_teams = jje_main_functions.get_users_teams_ids(guid)
        if not claim.yahoo_team.id in user_teams:
            return redirect(reverse('waivers_index'))

        claim.cancelled = True
        claim.save()
        messages.add_message(self.request, messages.INFO,
                             "Claim cancelled")
        email_functions.cancel_email(claim, request)
        return redirect(reverse('waivers_index'))
