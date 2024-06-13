# Generated by Django 4.2.4 on 2024-06-13 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0127_category_home_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="home_page_display",
            field=models.CharField(
                choices=[("approved", "Approved"), ("not approved", "Not Approved")],
                default="not approved",
                max_length=25,
            ),
        ),
    ]
