from django.db import models
from django.db import transaction

from galaxy_api.auth import models as auth_models


__all__ = ("Namespace", "NamespaceLink")


class Namespace(models.Model):
    """
    A model representing Ansible content namespace.

    Fields:
        name: Namespace name. Must be lower case containing only alphanumeric
            characters and underscores.
        company: Optional namespace owner company name.
        email: Optional namespace contact email.
        avatar_url: Optional namespace logo URL.
        description: Namespace brief description.

    Relations:
        owners: Reference to namespace owners.
        links: Back reference to related links.

    """

    # Fields

    name = models.CharField(max_length=64, unique=True, editable=False)
    company = models.CharField(max_length=64, blank=True)
    email = models.CharField(max_length=256, blank=True)
    avatar_url = models.CharField(max_length=256, blank=True)
    description = models.CharField(max_length=256, blank=True)

    # References
    owners = models.ManyToManyField(auth_models.Tenant, related_name="namespaces")

    def update_links(self, links):
        """Replace namespace related links with new ones."""
        db_links = [
            NamespaceLink(name=link["name"], url=link["url"], namespace=self)
            for link in links
        ]
        with transaction.atomic():
            self.links.all().delete()
            self.links.bulk_create(db_links)


class NamespaceLink(models.Model):
    """
    A model representing a Namespace link.

    Fields:
        name: Link name (e.g. Homepage, Documentation, etc.).
        url: Link URL.

    Relations:
        namespace: Reference to a parent namespace.
    """

    # Fields
    name = models.CharField(max_length=32)
    url = models.CharField(max_length=256)

    # References
    namespace = models.ForeignKey(
        Namespace, on_delete=models.CASCADE, related_name="links"
    )
