# Generated by Django 4.2.4 on 2024-07-22 06:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0164_remove_cartorderitems_price_wo_gst_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cartorderitems",
            old_name="price_wo_gst_total",
            new_name="price_wo_gst",
        ),
    ]