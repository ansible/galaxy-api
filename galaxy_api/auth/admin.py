from django.contrib import admin
from django.contrib.auth import admin as django_auth_admin
from galaxy_api.auth import models


@admin.register(models.User)
class UserAdmin(django_auth_admin.UserAdmin):
    pass


@admin.register(models.Group)
class GroupAdmin(django_auth_admin.GroupAdmin):
    pass
