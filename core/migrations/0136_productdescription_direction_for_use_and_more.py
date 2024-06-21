# Generated by Django 4.2.4 on 2024-06-18 16:45

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0135_product_yellow_peel"),
    ]

    operations = [
        migrations.AddField(
            model_name="productdescription",
            name="direction_for_use",
            field=tinymce.models.HTMLField(blank=True),
        ),
        migrations.AddField(
            model_name="productdescription",
            name="for_your_ease",
            field=tinymce.models.HTMLField(blank=True),
        ),
        migrations.AddField(
            model_name="productdescription",
            name="infusion_of_ingredients",
            field=tinymce.models.HTMLField(blank=True),
        ),
        migrations.AddField(
            model_name="productdescription",
            name="key_active_ingredients",
            field=tinymce.models.HTMLField(blank=True),
        ),
        migrations.AddField(
            model_name="productdescription",
            name="more_reasons_to_love",
            field=tinymce.models.HTMLField(blank=True),
        ),
        migrations.AddField(
            model_name="productdescription",
            name="reasons_to_love",
            field=tinymce.models.HTMLField(blank=True),
        ),
        migrations.AddField(
            model_name="productdescription",
            name="safety_warnings",
            field=tinymce.models.HTMLField(blank=True),
        ),
        migrations.AlterField(
            model_name="productdescription",
            name="product_description",
            field=tinymce.models.HTMLField(blank=True),
        ),
    ]