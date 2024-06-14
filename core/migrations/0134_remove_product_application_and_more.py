# Generated by Django 4.2.4 on 2024-06-14 07:11

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0133_remove_productvariationtypes_product_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="product", name="application",),
        migrations.RemoveField(model_name="product", name="deal_of_week",),
        migrations.RemoveField(model_name="product", name="description",),
        migrations.RemoveField(model_name="product", name="featured",),
        migrations.RemoveField(model_name="product", name="material",),
        migrations.RemoveField(model_name="product", name="specifications",),
        migrations.RemoveField(model_name="product", name="unit_item",),
        migrations.AddField(
            model_name="product",
            name="youtube_content",
            field=models.CharField(default="100percent free from..", max_length=12000),
        ),
        migrations.AddField(
            model_name="product",
            name="youtube_link",
            field=models.CharField(default="youtube video link..", max_length=12000),
        ),
        migrations.CreateModel(
            name="ProductDescription",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("product_description", tinymce.models.HTMLField()),
                (
                    "product",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="core.product",
                    ),
                ),
            ],
            options={"verbose_name_plural": "Product Description",},
        ),
    ]
