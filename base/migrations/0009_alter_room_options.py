# Generated by Django 4.2.3 on 2023-08-03 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_remove_room_likedby_room_likedby'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['-likes', '-created']},
        ),
    ]