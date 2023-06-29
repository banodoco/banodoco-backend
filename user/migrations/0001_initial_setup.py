# Generated by Django 3.2 on 2023-06-29 14:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('name', models.CharField(default='', max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('password', models.TextField(default=None, null=True)),
                ('type', models.CharField(default='user', max_length=50)),
                ('third_party_id', models.CharField(default=None, max_length=255, null=True)),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
