# Generated by Django 3.2 on 2023-06-29 14:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('token', models.TextField()),
                ('refresh_token', models.TextField()),
                ('role_id', models.CharField(max_length=50)),
                ('role_type', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'session',
            },
        ),
    ]