# Generated by Django 2.1.5 on 2019-03-10 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0021_extend_location_length'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lunauser',
            name='city',
        ),
    ]