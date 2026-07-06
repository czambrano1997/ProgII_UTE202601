from django.db import migrations, models
import django.db.models.deletion


def create_default_categories(apps, schema_editor):
    Categoria = apps.get_model("tienda", "Categoria")
    Categoria.objects.get_or_create(nombre="General", defaults={"descripcion": "Categoría por defecto"})


class Migration(migrations.Migration):
    dependencies = [
        ("tienda", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Categoria",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=100)),
                ("descripcion", models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name="producto",
            name="categoria",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="productos", to="tienda.categoria"),
        ),
        migrations.RunPython(create_default_categories, migrations.RunPython.noop),
    ]
