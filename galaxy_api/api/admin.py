from django.contrib import admin
from galaxy_api.api import models as api_models


@admin.register(api_models.Namespace)
class NamespaceAdmin(admin.ModelAdmin):
    fields = ('name', 'company', 'email', 'avatar_url', 'description', 'groups')
