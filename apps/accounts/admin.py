from django.contrib import admin

from .models import Credentials


class CredentialsAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user']

admin.site.register(Credentials, CredentialsAdmin)
