# Generated by Django 3.2 on 2023-09-04 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_project', '0005_model_type_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timing',
            name='strength',
            field=models.FloatField(default=1),
        ),
    ]