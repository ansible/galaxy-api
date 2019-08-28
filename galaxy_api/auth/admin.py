from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from galaxy_api.auth import models
from galaxy_api.api import models as api_models


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    pass


@admin.register(models.Tenant)
class TenantAdmin(admin.ModelAdmin):
    pass
