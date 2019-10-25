from django.contrib import admin
from galaxy_api.api import models as api_models


@admin.register(api_models.Namespace)
class NamespaceAdmin(admin.ModelAdmin):
    fields = ('name', 'company', 'email', 'avatar_url', 'description', 'groups')


@admin.register(api_models.NamespaceLink)
class NamespaceLinkAdmin(admin.ModelAdmin):
    fields = ('name', 'url', 'namespace')


@admin.register(api_models.CollectionImport)
class CollectionImportAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'created_at', 'namespace', 'name', 'version')
    fields = ('task_id', 'created_at', 'namespace', 'name', 'version')
    readonly_fields = ('name', 'version')
    date_hierarchy = 'created_at'
    search_fields = ['namespace__name', 'namespace__company', 'name']
    view_on_site = True
