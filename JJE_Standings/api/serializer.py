from rest_framework import serializers


from JJE_Standings.models import YahooStanding

from JJE_Waivers.api.serializer import YahooTeamSerializer

class YahooStandingSerializer(serializers.ModelSerializer):
    team = YahooTeamSerializer()

    class Meta:
        model = YahooStanding
        fields = (
            'team',
            'rank',
            'stat_point_total',
            'standings_week',
        )
