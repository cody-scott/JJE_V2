import django_filters

from allauth.account.models import EmailAddress


class EmailFilter(django_filters.FilterSet):
    user__is_staff = django_filters.BooleanFilter(field_name='user__is_staff')

    class Meta:
        model = EmailAddress
        fields = [
            'user__is_staff',
        ]
