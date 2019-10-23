from django.contrib import admin

# Register your models here.
from Yahoo_OAuth.models import UserToken


class UserTokenAdmin(admin.ModelAdmin):
    list_display = ['user',]


admin.site.register(UserToken, UserTokenAdmin)
