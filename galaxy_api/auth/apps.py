from django import apps


class AppConfig(apps.AppConfig):
    name = 'galaxy_api.auth'
    label = 'galaxy_auth'
