from rest_framework import serializers
from JJE_Standings.models import YahooStanding, YahooGUID, YahooTeam

# region Serializers for Complete Standings Data
class YahooStandingsAllStandingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = YahooStanding
        fields = (
            'standings_week',
            'rank',
            'stat_point_total',
        )


class YahooTeamAllStandingsSerializer(serializers.ModelSerializer):
    standings = YahooStandingsAllStandingsSerializer(many=True)
    class Meta:
        model = YahooTeam
        fields = (
            'team_id',
            'team_name',
            'standings',

        )
# endregion


# region this returns current rank and team flattened
class YahooRankSerializer(serializers.ModelSerializer):
    team_id = serializers.CharField(source='yahoo_team.team_id')
    team_name = serializers.CharField(source='yahoo_team.team_name')
    logo_url = serializers.URLField(source='yahoo_team.logo_url')
    current_rank = serializers.IntegerField(source='rank')

    class Meta:
        model = YahooStanding
        fields = (
            'team_id', 'team_name', 'current_rank', 'stat_point_total', 'standings_week', 'logo_url',
        )
# endregion


# region Serializer returns GUID -> Team -> standings (hyperlinked)
class YahooTeamHyperlinked(serializers.ModelSerializer):
    standings = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='all_standings-detail'
    )

    class Meta:
        model = YahooTeam
        fields = (
            'team_id', 'team_name', 'standings',
        )


class YahooGUIDSerializer(serializers.ModelSerializer):
    yahoo_team = YahooTeamHyperlinked(many=True, read_only=True)

    class Meta:
        model = YahooGUID

        fields = (
            'manager_name',
            'yahoo_guid',
            'yahoo_team',
        )
# endregion


# region These are just for the Team Name -> GUID
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
            'team_id',
            'team_name',
            'guid_teams',
        )
# endregion


# region These return the GUID -> Team with current ranking of that team
class YahooTeamCurrentSerializer(serializers.ModelSerializer):
    # current_standing = serializers.IntegerField(source='standings.id')
    current_standing = serializers.SerializerMethodField('get_current_standings')

    def get_current_standings(self, obj):
        c_rank = obj.standings.get(current_standings=True).rank
        return c_rank

    class Meta:
        model = YahooTeam
        # fields = (
        #     "id", 'team_id', 'team_name', 'logo_url',
        #     'current_standing',
        # )
        fields = (
            'team_id',
            'team_name',
            'current_standing',
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
# endregion