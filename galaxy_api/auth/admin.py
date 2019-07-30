from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from galaxy_api.auth import models


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    pass
