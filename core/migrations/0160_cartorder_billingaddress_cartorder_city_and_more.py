# Generated by Django 4.2.4 on 2024-07-21 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0159_cartorderitems_billingaddress_cartorderitems_city_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartorder",
            name="billingaddress",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorder",
            name="city",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorder",
            name="companyname",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorder",
            name="district",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorder",
            name="division",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorder",
            name="email",
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name="cartorder",
            name="firstname",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorder",
            name="gstnumber",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorder",
            name="lastname",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorder",
            name="phone",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="cartorder",
            name="pin_details",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorder",
            name="shippingaddress",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorder",
            name="state",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="cartorder",
            name="zipcode",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]