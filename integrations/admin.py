from django.contrib import admin

from integrations.models import PlatformAccount, PlatformToken

admin.site.register(PlatformAccount)
admin.site.register(PlatformToken)