from django.conf import settings

from pulpcore.client import pulp_ansible


def get_configuration(config_class):
    return config_class(
        host="http://{host}:{port}".format(
            host=settings.PULP_API_HOST,
            port=settings.PULP_API_PORT
        ),
        username=settings.PULP_API_USER,
        password=settings.PULP_API_PASSWORD
    )


def get_pulp_ansible_client():
    configuration = get_configuration(pulp_ansible.Configuration)
    return pulp_ansible.ApiClient(configuration)
