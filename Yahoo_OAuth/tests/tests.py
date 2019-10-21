from django.test import TestCase
from Yahoo_OAuth.models import UserToken
from datetime import timedelta
# Create your tests here.


def create_user_token(user=None):
    token = UserToken()
    token.client_id = ""
    token.client_secret = ""
    token.access_token = ""
    token.refresh_token = ""
    token.session_handle = ""
    token.user_guid = ""
    token.user = user
    token.save()
    return token


class UserTokenTest(TestCase):
    def test_token_expired(self):
        token = create_user_token()
        new_time = token.date_created - timedelta(hours=5)
        UserToken.objects.filter(pk=token.id).update(date_created=new_time)
        token = UserToken.objects.first()

        self.assertEqual(token.expired, True)

    def test_token_not_expired(self):
        token = create_user_token()
        new_time = token.date_created - timedelta(minutes=5)
        UserToken.objects.filter(pk=token.id).update(date_created=new_time)
        token = UserToken.objects.first()

        self.assertEqual(token.expired, False)
