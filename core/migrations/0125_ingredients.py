# Generated by Django 4.2.4 on 2024-06-10 17:28

from django.db import migrations, models
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0124_alter_cartorder_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ingredients",
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
                (
                    "iid",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="abcdefgh12345",
                        length=22,
                        max_length=30,
                        prefix="main_cat",
                        unique=True,
                    ),
                ),
                ("ingredient_title", models.CharField(max_length=100)),
                ("description", models.CharField(default="N/A", max_length=500)),
                ("meta_description", models.CharField(default="N/A", max_length=100)),
                ("meta_title", models.CharField(default="N/A", max_length=100)),
                ("meta_tag", models.CharField(default="N/A", max_length=100)),
                (
                    "active_status",
                    models.CharField(
                        choices=[("disabled", "Disabled"), ("published", "Published")],
                        default="disabled",
                        max_length=10,
                    ),
                ),
                (
                    "image",
                    models.ImageField(default="maincategory.jpg", upload_to="category"),
                ),
                (
                    "banner_image",
                    models.ImageField(
                        default="maincategorybanner.jpg", upload_to="category"
                    ),
                ),
            ],
            options={"verbose_name_plural": "Shop Ingredients",},
        ),
    ]
