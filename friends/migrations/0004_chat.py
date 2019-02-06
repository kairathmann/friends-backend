# Generated by Django 2.1.5 on 2019-02-05 13:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0003_auto_20190130_1046'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initial_type', models.PositiveSmallIntegerField(choices=[(1, 'Free'), (2, 'Text'), (3, 'Longtext'), (4, 'Video')])),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Free'), (2, 'Text'), (3, 'Longtext'), (4, 'Video')])),
                ('round', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='friends.Round')),
                ('users', models.ManyToManyField(related_name='chats', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]