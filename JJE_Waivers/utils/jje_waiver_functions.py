from django.utils import timezone
from datetime import timedelta

from JJE_Waivers.models import WaiverClaim


def get_active_claims():
    now = timezone.now() - timedelta(days=1)
    claims = WaiverClaim.objects \
        .filter(cancelled=False) \
        .filter(overclaimed=False) \
        .filter(claim_start__gt=now) \
        .order_by('claim_start')
    return claims


def show_oauth_link(request):
    """If both pass aka have a link, then dont show oauth link (AKA False)"""
    user = request.user
    if user.is_anonymous:
        return False

    if len(request.user.usertoken_set.all()) == 0:
        return True

    return False
