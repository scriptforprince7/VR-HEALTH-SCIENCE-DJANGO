# Generated by Django 4.2.4 on 2024-07-17 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0154_alter_cartorder_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="testimonials",
            name="testimonial_image",
            field=models.ImageField(
                default="testimonial.jpg", upload_to="blogs-images"
            ),
        ),
    ]