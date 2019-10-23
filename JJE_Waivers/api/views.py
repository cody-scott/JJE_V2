from rest_framework import viewsets, permissions
from rest_framework.response import Response

from JJE_Waivers.api import serializer
from JJE_Waivers.models import YahooGUID


# Returns GUID -> teams with current weekly rank of that team
class YahooTeamGUIDViewSetCurrentWeek(viewsets.ReadOnlyModelViewSet):
    queryset = YahooGUID.objects.all()
    serializer_class = serializer.YahooCurrentGUIDSerializer

    filterset_fields = (
        'yahoo_guid',
    )

    permission_classes = [permissions.IsAuthenticated]
