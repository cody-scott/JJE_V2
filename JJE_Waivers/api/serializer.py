from rest_framework import serializers
from JJE_Waivers.models import YahooGUID, YahooTeam#


class YahooTeamCurrentSerializer(serializers.ModelSerializer):
    class Meta:
        model = YahooTeam
        fields = (
            'id',
            'team_id',
            'team_name',
        )


class YahooCurrentGUIDSerializer(serializers.ModelSerializer):
    yahoo_team = YahooTeamCurrentSerializer(many=True)

    class Meta:
        model = YahooGUID

        fields = (
            'manager_name',
            'yahoo_guid',
            'yahoo_team',
        )
