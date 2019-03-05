# Generated by Django 2.1.5 on 2019-02-27 16:13

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0012_create_brian_bot'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedbackQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, unique=True)),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Rating'), (2, 'Text')])),
                ('is_enabled', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='FeedbackResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating_response', models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('text_response', models.TextField(null=True)),
                ('chat_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='friends.ChatUsers')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback_responses', to='friends.FeedbackQuestion')),
            ],
        ),
        migrations.AlterModelOptions(
            name='feedbackquestion',
            options={'ordering': ['order_index']},
        ),
        migrations.AddField(
            model_name='feedbackquestion',
            name='order_index',
            field=models.PositiveSmallIntegerField(db_index=True, default=1, unique=True),
            preserve_default=False,
        ),
    ]
