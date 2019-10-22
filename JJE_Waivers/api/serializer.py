# from rest_framework import serializers
#
# from JJE_Waivers import models
#
# from django.contrib.auth.models import User
#
#
# class YahooTeamSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.YahooTeam
#         fields = (
#             'id',
#             'team_name',
#             'logo_url',
#         )
#
#
# class WaiverClaimSerializer(serializers.ModelSerializer):
#     active_claim_field = serializers.BooleanField(source='active_claim')
#     team = YahooTeamSerializer()
#
#     class Meta:
#         model = models.WaiverClaim
#         fields = (
#             'id', 'team', 'claim_start',
#             'add_player', 'add_LW', 'add_C', 'add_RW', 'add_D', 'add_G', 'add_Util', 'add_IR',
#             'drop_player', 'drop_LW', 'drop_C', 'drop_RW', 'drop_D', 'drop_G', 'drop_Util', 'drop_IR',
#             'over_claim_id', 'overclaimed', 'cancelled', 'claim_message',
#             'get_position_add', 'get_position_drop',
#             'claim_end', 'claim_end_normal',
#             'active_claim_field',
#         )
#         read_only_fields = (
#             'active_claim_field',
#         )
#
#
