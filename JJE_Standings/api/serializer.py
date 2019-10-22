from rest_framework import serializers
from JJE_Standings.models import YahooStanding, YahooGUID, YahooTeam


class YahooStandingSerializer(serializers.ModelSerializer):
    class Meta:
        model = YahooStanding
        fields = (
            'rank',
            'stat_point_total',
            'standings_week',
        )


# this returns current rank and team flattened
class YahooRankSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='yahoo_team.team_name')
    current_rank = serializers.IntegerField(source='rank')

    class Meta:
        model = YahooStanding
        fields = (
            'team_name', 'current_rank', 'stat_point_total', 'standings_week',
        )


class YahooTeamRankSerializer(serializers.ModelSerializer):
    standings = YahooStandingSerializer(many=True)
    class Meta:
        model = YahooTeam
        fields = (
            'team_name',
            'standings'
        )


class YahooGUIDSerializer(serializers.ModelSerializer):
    yahoo_team = YahooTeamRankSerializer(many=True, read_only=True)

    class Meta:
        model = YahooGUID

        fields = (
            'manager_name',
            'yahoo_guid',
            'yahoo_team',
        )


class SimpleYahooGUIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = YahooGUID

        fields = (
            'manager_name',
            'yahoo_guid',
        )


class YahooTeamtoGUID(serializers.ModelSerializer):
    guid_teams = SimpleYahooGUIDSerializer(many=True)

    class Meta:
        model = YahooTeam

        fields = (
            'team_name',
            'guid_teams',
        )