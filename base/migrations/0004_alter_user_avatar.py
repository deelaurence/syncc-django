# Generated by Django 4.2.3 on 2023-07-31 08:17

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=cloudinary.models.CloudinaryField(default='avatar.jpeg', max_length=255, verbose_name='avatar'),
        ),
    ]
