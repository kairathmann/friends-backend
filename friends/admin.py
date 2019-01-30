from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from . import models


class RoundAdmin(admin.ModelAdmin):
    model = models.Round
    exclude = ('users', )


# Register
admin.site.register(models.Round, RoundAdmin)

# Unregister
admin.autodiscover()
admin.site.unregister(Group)
admin.site.unregister(Token)
