# Generated by Django 3.2 on 2023-07-31 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_project', '0003_temp_file_list_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='aimodel',
            name='custom_trained',
            field=models.BooleanField(default=False),
        ),
    ]