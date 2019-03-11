# Generated by Django 2.1.5 on 2019-03-11 15:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0022_remove_lunauser_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneVerificationExemption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_code', models.CharField(max_length=5)),
                ('phone_number', models.CharField(max_length=18)),
                ('token', models.CharField(max_length=4)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
