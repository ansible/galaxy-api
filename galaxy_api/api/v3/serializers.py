import mimetypes

from rest_framework import serializers

from galaxy_api.api.utils import parse_collection_filename


class CollectionSerializer(serializers.Serializer):

    name = serializers.CharField(required=True)
    namespace = serializers.CharField(required=True)

    deprecated = serializers.BooleanField(required=False)


class CollectionUploadSerializer(serializers.Serializer):
    """
    A serializer for the Collection One Shot Upload API.
    """

    file = serializers.FileField(required=True)

    sha256 = serializers.CharField(required=False, default=None)

    def to_internal_value(self, data):
        """Parse and validate collection filename."""
        data = super().to_internal_value(data)

        filename = data["file"].name
        data.update({
            "filename": parse_collection_filename(filename),
            "mimetype": (mimetypes.guess_type(filename)[0] or 'application/octet-stream')
        })
        return data
