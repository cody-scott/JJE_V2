from rest_framework import serializers
from JJE_Standings.models import YahooStanding, YahooGUID, YahooTeam


class YahooTeamSerializer(serializers.ModelSerializer):
    standings = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = YahooTeam
        fields = (
            'team_id',
            'team_name',
            'logo_url',
            'standings',
        )


class YahooStandingSerializer(serializers.ModelSerializer):
    yahoo_team = YahooTeamSerializer()

    class Meta:
        model = YahooStanding
        fields = (
            'yahoo_team',
            'rank',
            'stat_point_total',
            'standings_week',
        )


class YahooGUIDSerializer(serializers.ModelSerializer):
    yahoo_team = YahooTeamSerializer(many=True, read_only=True)

    class Meta:
        model = YahooGUID

        fields = (
            'manager_name',
            'yahoo_guid',
            'yahoo_team',
        )
