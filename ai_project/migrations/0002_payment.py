# Generated by Django 3.2 on 2023-07-01 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_project', '0001_initial_setup'),
    ]

    operations = [
        migrations.AddField(
            model_name='inferencelog',
            name='total_credits_used',
            field=models.FloatField(default=0),
        ),
    ]
