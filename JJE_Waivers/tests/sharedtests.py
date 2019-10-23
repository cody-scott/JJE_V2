# from django.contrib.auth import get_user_model
#
# from JJE_Waivers.models import YahooTeam, WaiverClaim
#
#
# def create_test_user(username="test@test.com", password='test'):
#     User = get_user_model()
#     user = User.objects.create_user(
#         username, password=password, email=username, is_active=True
#     )
#     return user
#
#
# def create_test_user_login(client, username="test@test.com", user_pass='test'):
#     user = create_test_user(username, user_pass)
#     logged_in = client.login(
#         username=username,
#         password=user_pass)
#     return user, logged_in
#
#
# def create_test_team(team_name, user=None):
#     new_team = YahooTeam()
#     new_team.team_name = team_name
#     if user is not None:
#         new_team.user = user
#     new_team.save()
#     return new_team
#
#
# def create_claim(add_player, drop_player, team):
#     claim = WaiverClaim()
#     claim.add_player = add_player
#     claim.add_C = True
#     claim.drop_player = drop_player
#     claim.drop_C = True
#     claim.team = team
#     claim.save()
#     return claim
