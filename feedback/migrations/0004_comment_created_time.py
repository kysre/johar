# Generated by Django 3.2.20 on 2023-11-23 17:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]