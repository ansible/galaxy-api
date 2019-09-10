from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("galaxy_api", "0004_namespace_groups")]

    operations = [
        migrations.CreateModel(
            name="CollectionImport",
            fields=[
                ("task_id", models.UUIDField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField()),
                ("name", models.CharField(editable=False, max_length=64)),
                ("version", models.CharField(editable=False, max_length=32)),
                (
                    "namespace",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="galaxy_api.Namespace",
                    ),
                ),
            ],
            options={'ordering': ['-task_id']},
        )
    ]
