# Generated by Django 4.2.4 on 2024-07-21 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0158_alter_cartorder_courier_partner_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartorderitems",
            name="billingaddress",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorderitems",
            name="city",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorderitems",
            name="companyname",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorderitems",
            name="district",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorderitems",
            name="division",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorderitems",
            name="email",
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name="cartorderitems",
            name="firstname",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorderitems",
            name="gstnumber",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorderitems",
            name="lastname",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorderitems",
            name="phone",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="cartorderitems",
            name="pin_details",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorderitems",
            name="shippingaddress",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorderitems",
            name="state",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorderitems",
            name="zipcode",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]