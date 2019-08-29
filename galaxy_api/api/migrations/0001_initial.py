from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    initial = True

    dependencies = [("galaxy_auth", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Namespace",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64, unique=True)),
                ("company", models.CharField(blank=True, max_length=64)),
                ("email", models.CharField(blank=True, max_length=256)),
                ("avatar_url", models.CharField(blank=True, max_length=256)),
                ("description", models.CharField(blank=True, max_length=256)),
                (
                    "owners",
                    models.ManyToManyField(
                        related_name="namespaces", to="galaxy_auth.Tenant"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="NamespaceLink",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=32)),
                ("url", models.CharField(max_length=256)),
                (
                    "namespace",
                    models.ForeignKey(
                        on_delete=models.CASCADE,
                        related_name="links",
                        to="galaxy_api.Namespace",
                    ),
                ),
            ],
        ),
    ]
