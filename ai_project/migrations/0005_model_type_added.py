# Generated by Django 3.2 on 2023-08-25 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_project', '0004_custom_trained_model_check_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='aimodel',
            name='model_type',
            field=models.TextField(blank=True, default=''),
        ),
    ]