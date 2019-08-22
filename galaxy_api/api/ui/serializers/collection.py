from rest_framework import serializers

from .namespace import NamespaceSerializer


# TODO: Aggregate contents by type (Example data from David needed)
#   class ContentSummary {
#       total_count: number;
#       contents: {
#           module: string[];
#           role: string[];
#           plugin: string[];
#           playbook: string[];
#       };
#   }


class CollectionMetadataBaseSerializer(serializers.Serializer):
    description = serializers.CharField()
    authors = serializers.ListField(serializers.CharField())
    license = serializers.ListField(serializers.CharField())
    tags = serializers.SerializerMethodField()

    def get_tags(self, metadata):
        return [tag['name'] for tag in metadata['tags']]


class CollectionMetadataSerializer(CollectionMetadataBaseSerializer):
    dependencies = serializers.JSONField()
    contents = serializers.JSONField()

    # URLs
    documentation = serializers.CharField()
    homepage = serializers.CharField()
    issues = serializers.CharField()
    repository = serializers.CharField()


class CollectionVersionBaseSerializer(serializers.Serializer):
    namespace = serializers.CharField()
    name = serializers.CharField()
    version = serializers.CharField()
    created_at = serializers.DateTimeField(source='_created')


class CollectionVersionAndBaseMetadataSerializer(CollectionVersionBaseSerializer):
    metadata = CollectionMetadataBaseSerializer(source='*')


class CollectionVersionSerializer(CollectionMetadataBaseSerializer):
    metadata = CollectionMetadataSerializer(source="*")
    docs_blob = serializers.JSONField()


class CollectionSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    namespace = serializers.SerializerMethodField()
    name = serializers.CharField()
    download_count = serializers.IntegerField(default=0)

    latest_version = CollectionVersionAndBaseMetadataSerializer(source='*')

    def get_id(self, obj):
        return f"{obj['namespace']}.{obj['name']}"

    def get_namespace(self, obj):
        namespace = obj['namespace']
        if 'namespace_dict' in self.context:
            namespace = self.context['namespace_dict'][namespace]
        else:
            namespace = self.context['namespace']

        return NamespaceSerializer(namespace).data
