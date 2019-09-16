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
        fields = (
            'id',
            'name',
            'company',
            'email',
            'avatar_url',
            'description',
            'links',
            'resources'
        )
        read_only_fields = ('name', )

    @transaction.atomic
    def update(self, instance, validated_data):
        links = validated_data.pop('links', None)

        instance = super().update(instance, validated_data)

        if links is not None:
            instance.set_links(links)

        return instance


class NamespaceSummarySerializer(NamespaceSerializer):
    '''NamespaceSerializer but without 'links' or 'resources'

    For use in _ui/collection detail views.'''

    class Meta:
        model = models.Namespace
        fields = (
            'id',
            'name',
            'company',
            'email',
            'avatar_url',
            'description',
        )
        read_only_fields = ('name', )
