# Generated by Django 4.2.3 on 2023-08-03 22:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_alter_room_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['-created', '-likes']},
        ),
    ]
