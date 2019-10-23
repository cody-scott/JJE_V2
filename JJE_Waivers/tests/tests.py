# import datetime
#
# from django.contrib.auth import get_user_model
# from django.test import TestCase
# from django.urls import reverse
# from django.utils import timezone
#
# from JJE_Standings.tests.shared_tests import create_standing
# from JJE_Waivers.models import WaiverClaim, YahooTeam
# from JJE_Waivers.tests.sharedtests import \
#     create_test_user, create_test_user_login, create_test_team, create_claim
#
#
# from JJE_oauth.tests.tests import create_user_token
#
#
# class YahooTeamTest(TestCase):
#     def test_new_team(self):
#         team = create_test_team("Team 1")
#         teams = YahooTeam.objects.all()
#         self.assertCountEqual(teams, [team])
#
#
# class WaiverClaimTest(TestCase):
#     def test_claim_active(self):
#         claim = WaiverClaim()
#         self.assertIs(claim.active_claim(), True)
#
#     def test_old_claim_inactive(self):
#         claim = WaiverClaim()
#         old_time = timezone.now() - datetime.timedelta(days=2)
#         claim.claim_start = old_time
#         self.assertIs(claim.active_claim(), False)
#
#     def test_cancel_claim(self):
#         claim = WaiverClaim()
#         claim.cancelled = True
#         self.assertIs(claim.active_claim(), False)
#
#     def test_overclaim(self):
#         claim = WaiverClaim()
#         claim.overclaimed = True
#         self.assertIs(claim.active_claim(), False)
#
#     def test_add_position(self):
#         claim = WaiverClaim()
#         claim.add_C = True
#         claim.add_D = True
#         self.assertEqual(claim.get_position_add, 'C/D')
#
#     def test_drop_position(self):
#         claim = WaiverClaim()
#         claim.drop_IR = True
#         self.assertEqual(claim.get_position_drop, 'IR')
#
#     def test_claim_end(self):
#         claim = WaiverClaim()
#         st = timezone.now()
#         et = (st + datetime.timedelta(days=1)).isoformat()
#         claim.claim_start = st
#         # claim.save()
#         self.assertEqual(claim.claim_end, et)
#
#
# class IndexViewTest(TestCase):
#     def test_index_no_claim(self):
#         response = self.client.get(reverse("index"))
#         self.assertQuerysetEqual(response.context['waiverclaim_list'], [])
#
#     def test_index_one_claim(self):
#         st = (timezone.now() - datetime.timedelta(hours=5))
#         team = create_test_team("Test")
#         claim = create_claim("Test Player Add", "Test Player Drop", team)
#         response = self.client.get(reverse("index"))
#         self.assertQuerysetEqual(
#             response.context['waiverclaim_list'],
#             ["<WaiverClaim: Test Player Add>"]
#         )
#
#     def test_index_two_claims(self):
#         team = create_test_team("Test Team")
#         claim_one = create_claim("Test A P 1", "Test D P 1", team)
#         claim_two = create_claim("Test A P 2", "Test D P 2", team)
#         response = self.client.get(reverse("index"))
#         self.assertQuerysetEqual(
#             response.context['waiverclaim_list'],
#             ["<WaiverClaim: Test A P 1>", "<WaiverClaim: Test A P 2>"],
#             ordered=False
#         )
#
#     def test_old_and_new_claims(self):
#         team = create_test_team("Test Team")
#         claim_one = create_claim("Test A P 1", "Test D P 1", team)
#         claim_two = create_claim("Test A P 2", "Test D P 2", team)
#         claim_one.claim_start = (timezone.now() - datetime.timedelta(days=2))
#         claim_one.save()
#         response = self.client.get(reverse("index"))
#         self.assertQuerysetEqual(
#             response.context['waiverclaim_list'],
#             ["<WaiverClaim: Test A P 2>"],
#             ordered=False
#         )
#
#     def test_anonymous_no_new_claim_button(self):
#         request = self.client.get('/')
#         check = False
#         self.assertNotIn(
#             '<input type="submit" class="newclaim_btn" value="New Claim">',
#             request.rendered_content
#         )
#
#
# class IndexViewLoggedInTest(TestCase):
#     def test_valid_login(self):
#         user = create_test_user_login(self.client)
#         User = get_user_model()
#         first_user = User.objects.first()
#         self.assertEqual(user, (first_user, True, ))
#
#     def test_valid_claims(self):
#         user, logged_in = create_test_user_login(self.client)
#         team = create_test_team("Test Team", user)
#         second_team = create_test_team("second_team", user)
#         claim_one = create_claim("Test A P 1", "Test D P 1", team)
#         x = [user.yahooteam_set.first().waiverclaim_set.first()]
#         z = [WaiverClaim.objects.filter(team=team.id).first()]
#         self.assertEqual(x, z)
#
#     def test_cancel_valid_html(self):
#         user, logged_in = create_test_user_login(self.client)
#         team = create_test_team("Test Team", user)
#         claim_one = create_claim("Test A P 1", "Test D P 1", team)
#         request = self.client.get('/')
#         self.assertInHTML(
#             '<input class="btn btn-danger cancel_btn" type="submit" value="Cancel">',
#             request.rendered_content
#         )
#
#     def test_cancel_missing_from_current_user(self):
#         user1 = create_test_user()
#         user2, logged_in = create_test_user_login(
#             self.client, "test1@test.com", "test"
#         )
#
#         t1 = create_test_team("Team1", user1)
#         t2 = create_test_team("Team2", user2)
#
#         claim = create_claim("Test", "Test", t1)
#
#         request = self.client.get("/")
#         check = False
#         self.assertNotIn(
#             '<input class="cancel_btn" type="submit" value="Cancel">',
#             request.rendered_content
#         )
#
#     def test_oauth_registration_link_visible(self):
#         user, logged_in = create_test_user_login(self.client)
#         request = self.client.get('/')
#         self.assertInHTML(
#             '<input type="submit" class="btn btn-success newclaim_btn" value="Link Yahoo">',
#             request.rendered_content
#         )
#
#     def test_oauth_registration_link_hidden(self):
#         user, logged_in = create_test_user_login(self.client)
#         team = create_test_team("test", user)
#         token = create_user_token(user)
#         request = self.client.get('/')
#         self.assertInHTML(
#             '<input type="submit" class="btn btn-success newclaim_btn" value="New Claim">',
#             request.rendered_content
#         )
#
#     def test_overclaim_valid_html_no_standings(self):
#         user1 = create_test_user()
#         user2, logged_in = create_test_user_login(
#             self.client, "test1@test.com", "test"
#         )
#
#         t1 = create_test_team("Team1", user1)
#         t2 = create_test_team("Team2", user2)
#
#         claim = create_claim("Test", "Test", t1)
#
#         request = self.client.get('/')
#         self.assertNotIn(
#             '<input class="btn btn-primary overclaim_btn" type="submit" value="Overclaim">',
#             request.rendered_content
#         )
#
#
# class OverclaimViewTest(TestCase):
#     """
#     Tests
#     not logged in
#     overclaim of no id
#     overclaim of same team
#     overclaim of lower rank
#     overclaim of same rank
#     overclaim of higher rank
#     overclaim id check
#     """
#
#
#     def test_null_overclaim(self):
#         """
#         Waiver claim matching query because requesting
#         this section for an item that doesn't exist
#         """
#         user2, logged_in = create_test_user_login(
#             self.client, "test1@test.com", "test")
#         team = create_test_team("Test Team", user2)
#         claim_one = create_claim("Test A P 1", "Test D P 1", team)
#         response = self.client.get('/waiver_claim/overclaim={}'.format(9999))
#         self.assertEqual(response.status_code, 302)
#
#
#     def test_valid_overclaim(self):
#         user, logged_in = create_test_user_login(self.client)
#         team = create_test_team("Test Team", user)
#         create_standing(team)
#
#         claim_one = create_claim("Test A P 1", "Test D P 1", team)
#         response = self.client.get(f'/waiver_claim/overclaim={claim_one.id}')
#         self.assertEqual(response.status_code, 302)
#
#     def test_overclaim_content(self):
#         user = create_test_user()
#         user2, logged_in = create_test_user_login(
#             self.client, "test1@test.com", "test")
#         team = create_test_team("Test Team", user)
#         create_standing(team)
#
#         team2 = create_test_team("Test Team 2", user2)
#         claim_one = create_claim("Test A P 1", "Test D P 1", team)
#         response = self.client.get(f'/waiver_claim/overclaim={claim_one.id}')
#         self.assertEqual(response.context['add_name'], claim_one.add_player)
#
#     def test_overclaim_content_same_user(self):
#         """
#         Testing to see what happens if the same user tries and overclaims their own
#         Should redirect home?
#         :return:
#         """
#         user = create_test_user()
#         user2, logged_in = create_test_user_login(
#             self.client, "test1@test.com", "test")
#         team = create_test_team("Test Team", user)
#         create_standing(team)
#
#         team2 = create_test_team("Test Team 2", user2)
#         claim_one = create_claim("Test A P 1", "Test D P 1", team2)
#
#         response = self.client.get(f'/waiver_claim/overclaim={claim_one.id}')
#
#         self.assertEqual(response.context['add_name'], claim_one.add_player)
#
#     def test_overclaim_submit(self):
#         """
#         Check if overclaim id is valid when overclaiming
#         Second claim id should be the id of the first claim
#         first claim should also be flagged as overclaimed
#         :return:
#         """
#         user = create_test_user()
#         user2, logged_in = create_test_user_login(
#             self.client, "test1@test.com", "test")
#         team = create_test_team("Test Team", user)
#         team_two = create_test_team("Team Two", user2)
#
#         create_standing(team, 1)
#         create_standing(team_two, 2)
#         claim_one = create_claim("Test A P 1", "Test D P 1", team)
#
#         response = self.client.post(f'/waiver_claim/overclaim={claim_one.id}',
#                                     {
#                                         'team': team_two.id,
#                                         'drop_player': "Drop Test"}
#                                     )
#         claim_two = team_two.waiverclaim_set.first()
#
#         claim_one = WaiverClaim.objects.get(id=claim_one.id)
#         self.assertIs(claim_one.overclaimed, True)
#
#         self.assertEqual(claim_two.over_claim_id, claim_one.id)
#
#     def test_logged_in_overclaim(self):
#         """
#         Team 1 is lower rank then team 2
#         test to see if team 1 tries to overclaim team 2
#         goal is to ensure its able to get to the overclaim page
#         Testing to see if valid overclaim page
#         :return:
#         """
#         user, logged_in = create_test_user_login(
#             self.client, "t1@test.com", "pass")
#         team = create_test_team("t1", user)
#         create_standing(team, 2)
#
#         user2, logged_in = create_test_user_login(
#             self.client, "test1@test.com", "test")
#         team2 = create_test_team("t2", user2)
#         create_standing(team2, 1)
#
#         self.client.login(username="t1@test.com", password="pass")
#
#         claim = create_claim("ap1", "dp1", team2)
#
#         response = self.client.get(f"/waiver_claim/overclaim={claim.id}")
#         self.assertInHTML(
#             f'<option value="{team.id}" selected>t1</option>',
#             response.rendered_content)
#
#     def test_claim_by_higher_rank_team(self):
#         """
#         Team 1 is the higher team
#         test to see if team 1 tries to overclaim team 2
#         should redirect to home
#         :return:
#         """
#         user, logged_in = create_test_user_login(
#             self.client, "t1@test.com", "pass"
#         )
#         team = create_test_team("t1", user)
#         create_standing(team, 1)
#
#         user2 = create_test_user("t2@test.com", "pass")
#         team2 = create_test_team("t2", user2)
#         create_standing(team2, 3)
#
#         claim = create_claim("ap1", "dp1", team2)
#
#         response = self.client.get(f"/waiver_claim/overclaim={claim.id}")
#
#         self.assertEqual(response.status_code, 302)
#
#     def test_claim_by_equal_rank_team(self):
#         """
#         Team 1 and team 2 are equal ranked teams
#         test to see if team 1 tries to overclaim team 2
#         should redirect to home
#         :return:
#         """
#         user, logged_in = create_test_user_login(
#             self.client, "t1@test.com", "pass"
#         )
#         team = create_test_team("t1", user)
#         create_standing(team, 1)
#
#         user2 = create_test_user("t2@test.com", "pass")
#         team2 = create_test_team("t2", user2)
#         create_standing(team2, 1)
#
#         claim = create_claim("ap1", "dp1", team2)
#
#         response = self.client.get(f"/waiver_claim/overclaim={claim.id}")
#
#         self.assertEqual(response.status_code, 302)
#
#     def test_claim_by_lower_rank_team(self):
#         user, logged_in = create_test_user_login(
#             self.client, "t1@test.com", "pass"
#         )
#         team = create_test_team("t1", user)
#         create_standing(team, 2)
#
#         user2 = create_test_user("t2@test.com", "pass")
#         team2 = create_test_team("t2", user2)
#         create_standing(team2, 1)
#
#         claim = create_claim("ap1", "dp1", team2)
#
#         response = self.client.get(f"/waiver_claim/overclaim={claim.id}")
#
#         self.assertEqual(response.status_code, 200)
#
#
# class NewClaimTest(TestCase):
#     def test_null_submission_team(self):
#         user, logged_in = create_test_user_login(
#             self.client, "t1@test.com", "pass")
#         team = create_test_team("t1", user)
#         response = self.client.post('/waiver_claim/new/',
#                                     {
#                                         'add_player': "Test A",
#                                         'add_C': True,
#                                         'drop_player': "Test D",
#                                     }, follow=True)
#         self.assertEqual(response.redirect_chain, [])
#
#
# class CancelClaimTest(TestCase):
#     def test_valid_cancel_post(self):
#         user, logged_in = create_test_user_login(self.client)
#         team = create_test_team("Test Team", user)
#         claim_one = create_claim("Test A P 1", "Test D P 1", team)
#         response = self.client.post(
#             '/waiver_claim/cancel={}'.format(claim_one.id), follow=True)
#         claim_one_test = WaiverClaim.objects.get(id=claim_one.id)
#         self.assertIs(claim_one_test.cancelled, True)
#
#     def test_cancel_wrong_user_post(self):
#         user, logged_in = create_test_user_login(self.client)
#         team = create_test_team("Test Team", user)
#         claim_one = create_claim("Test A P 1", "Test D P 1", team)
#         user2, logged_in = create_test_user_login(
#             username="test2@test.com", user_pass="pass", client=self.client)
#         response = self.client.post(
#             '/waiver_claim/cancel={}'.format(claim_one.id), follow=True
#         )
#         claim_one_test = WaiverClaim.objects.get(id=1)
#         self.assertIs(claim_one_test.cancelled, False)
#
#
# class CancelClaimTestViews(TestCase):
#     def test_cancel_view(self):
#         user, logged_in = create_test_user_login(self.client)
#         team = create_test_team("Test Team", user)
#         claim_one = create_claim("Test A P 1", "Test D P 1", team)
#         response = self.client.get(
#             '/waiver_claim/cancel={}'.format(claim_one.id))
#         self.assertEqual(response.status_code, 200)
#
#     def test_cancel_wrong_user(self):
#         user, logged_in = create_test_user_login(self.client)
#         team = create_test_team("Test Team", user)
#         claim_one = create_claim("Test A P 1", "Test D P 1", team)
#         user2, logged_in = create_test_user_login(
#             username="test2@test.com", user_pass="pass", client=self.client
#         )
#         response = self.client.get(
#             '/waiver_claim/cancel={}'.format(claim_one.id)
#         )
#         self.assertEqual(response.status_code, 302)
#
#     def test_cancel_view_not_logged_in(self):
#         user = create_test_user()
#         team = create_test_team("Test Team", user)
#         claim_one = create_claim("Test A P 1", "Test D P 1", team)
#         response = self.client.get(
#             '/waiver_claim/cancel={}'.format(claim_one.id)
#         )
#         self.assertEqual(response.status_code, 302)
