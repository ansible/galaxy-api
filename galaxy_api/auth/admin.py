from django.contrib import admin
from django.contrib.auth import admin as django_auth_admin
from galaxy_api.auth import models


@admin.register(models.User)
class UserAdmin(django_auth_admin.UserAdmin):
    pass


class UserInLine(admin.TabularInline):
    model = models.Group.user_set.through
    fields = ('user', 'username', 'email_address', 'first_name', 'last_name',)
    readonly_fields = ('username', 'email_address', 'first_name', 'last_name',)

    verbose_name = "User"
    verbose_name_plural = "Group Members"

    autocomplete_fields = ['user']

    def username(self, instance):
        return instance.user.username

    def email_address(self, instance):
        return instance.user.email_address

    def first_name(self, instance):
        return instance.user.first_name

    def last_name(self, instance):
        return instance.user.last_name

    extra = 0


@admin.register(models.Group)
class GroupAdmin(django_auth_admin.GroupAdmin):
    inlines = [UserInLine]
