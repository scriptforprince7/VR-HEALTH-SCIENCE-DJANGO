# Generated by Django 4.2.4 on 2024-04-05 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0115_remove_productvariationtypes_varient_type_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="productvariationtypes",
            name="varient_type_price",
            field=models.DecimalField(decimal_places=2, default="1", max_digits=9999),
        ),
        migrations.AddField(
            model_name="productvarient",
            name="have_variation",
            field=models.BooleanField(default=False),
        ),
    ]
