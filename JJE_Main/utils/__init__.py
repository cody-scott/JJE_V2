from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def update_username_from_email(sender, instance, **kwargs):
    user_email = instance.email
    username = user_email[:30]
    n = 1
    while User.objects.exclude(pk=instance.pk).filter(username=username).exists():
        n += 1
        username = user_email[:(29 - len(str(n)))] + '-' + str(n)
    instance.username = username