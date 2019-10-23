# from django.test import TestCase
# from django.utils import timezone
# from django.urls import reverse
# from django.contrib.auth import get_user_model
#
# from JJE_Waivers.models import YahooTeam, WaiverClaim
# from JJE_Waivers import utils
# from JJE_Standings.models import YahooStanding
# from JJE_oauth.tests.tests import create_user_token
#
#
# def create_test_user(username="test@test.com", password='test'):
#     User = get_user_model()
#     user = User.objects.create_user(
#         username, password=password, email=username, is_active=True)
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
#
#
#
# class YahooTeamTest(TestCase):
#     def test_user_no_team_assigned(self):
#         """
#         This should return false as a user is created/logged in,
#         but no team assigned to that user
#         """
#         user, logged_in = create_test_user_login(self.client)
#         create_test_team("Test 1")
#
#         self.assertEqual(utils._check_user_team(user), False)
#
#     def test_user_team_assigned(self):
#         user, logged_in = create_test_user_login(self.client)
#         create_test_team("Test 1", user)
#
#         self.assertEqual(utils._check_user_team(user), True)
#
#     def test_user_no_token(self):
#         user, logged_in = create_test_user_login(self.client)
#         token = create_user_token()
#         self.assertEqual(utils._check_user_token(user), False)
#
#     def test_user_token(self):
#         user, logged_in = create_test_user_login(self.client)
#         token = create_user_token(user)
#         self.assertEqual(utils._check_user_token(user), True)
