# Generated by Django 4.2.4 on 2024-06-13 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0130_bannerhome_banner_image_alter_bannerhome_bhid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bannerhome",
            name="banner_title",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
