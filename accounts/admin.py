from django.contrib import admin
from . import models


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_confirmed', ]


admin.site.register(models.Profile, ProfileAdmin)
