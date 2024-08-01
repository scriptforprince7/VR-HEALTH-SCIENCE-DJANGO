# Generated by Django 4.2.4 on 2024-07-22 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0163_cartorderitems_gst_rates_final_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="cartorderitems", name="price_wo_gst",),
        migrations.AddField(
            model_name="cartorderitems",
            name="price_wo_gst_total",
            field=models.DecimalField(decimal_places=2, default="0", max_digits=99999),
        ),
    ]