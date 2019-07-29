from django.db import transaction

from rest_framework.serializers import ModelSerializer

from galaxy_api.api import models


class NamespaceLinkSerializer(ModelSerializer):
    class Meta:
        model = models.NamespaceLink
        fields = ('name', 'url')


class NamespaceSerializer(ModelSerializer):
    links = NamespaceLinkSerializer(many=True)

    class Meta:
        model = models.Namespace
        fields = ('name', 'company', 'email', 'avatar_url', 'description', 'links')
        read_only_fields = ('name', )

    def update(self, instance, validated_data):
        links = validated_data.pop('links')

        with transaction.atomic():
            instance = super().update(instance, validated_data)
            instance.update_links(links)

        return instance
