# Generated by Django 3.2 on 2023-11-26 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_project', '0011_log_mapped_to_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inferencelog',
            name='total_inference_time',
            field=models.FloatField(default=0),
        ),
    ]
