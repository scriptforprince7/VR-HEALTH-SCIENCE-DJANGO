# Generated by Django 4.2.4 on 2024-03-23 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0105_product_deal_of_week_product_new_arrival_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="productvarient",
            name="gst_rate",
            field=models.CharField(default="5%", max_length=12),
        ),
    ]
