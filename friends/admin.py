from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from . import models


# Register

# Unregister
admin.autodiscover()
admin.site.unregister(Group)
admin.site.unregister(Token)
