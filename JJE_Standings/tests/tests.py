from unittest import mock
from django.test import TestCase
from JJE_Standings import utils
from JJE_Standings.tests.shared_tests import create_standing
from JJE_Standings.utils import yahoo_data
from JJE_Waivers.tests.sharedtests import create_test_user, create_test_team

import json
# Create your tests here.


class mock_results:
    def __init__(self):
        self.text = self.load_text()
        self.status_code = 200

    def load_text(self):
        data = ""
        with open("JJE_Standings/tests/data.html", 'r') as file_reader:
            data = file_reader.read()
        return data


class mock_oauth:
    def get(self, *args, **kwargs):
        return mock_results()

    def request(self, *args, **kwargs):
        return self.get()


class StandingsTest(TestCase):
    def create_mock_item(self):
        return mock_oauth()

    @mock.patch("JJE_Standings.utils.yahoo_data.create_session",
                create_mock_item)
    def test_team_creation(self):
        yahoo_data.build_team_data(self.client.request)
        self.assertEqual(True, True)

    @mock.patch("JJE_Standings.utils.yahoo_data.create_session",
                create_mock_item)
    def test_standings_creation(self):
        yahoo_data._standings_collection(mock_oauth())
        self.assertEqual(True, True)

    def test_get_standings(self):
        u1 = create_test_user("user1@test.com", "pass")
        t1 = create_test_team("t1", u1)
        s1 = create_standing(t1, 1)

        u2 = create_test_user("user2@test.com", "pass")
        t2 = create_test_team("t2", u2)
        s2 = create_standing(t2, 2)

        standings = utils.get_standings()

        self.assertEqual(standings,
                         [
                             ['', 't1', 1, 0.0, ''],
                             ['', 't2', 2, 0.0, ''],
                         ])

    def test_get_standings_json(self):
        u1 = create_test_user("user1@test.com", "pass")
        t1 = create_test_team("t1", u1)
        s1 = create_standing(t1, 1)

        u2 = create_test_user("user2@test.com", "pass")
        t2 = create_test_team("t2", u2)
        s2 = create_standing(t2, 2)

        json_standings = utils.get_standings_json()
        test_struct = json.dumps([{
            "TeamID": "",
            "TeamName": t1.team_name,
            "TeamRank": 1,
            "TeamPoints": 0.0,
            "TeamURL": '',
            # "UserTeam": team_flag,
        },
            {
                "TeamID": '',
                "TeamName": t2.team_name,
                "TeamRank": 2,
                "TeamPoints": 0.0,
                "TeamURL": '',
                # "UserTeam": team_flag,
            },
        ], indent=4)

        self.assertEqual(json_standings, test_struct)
