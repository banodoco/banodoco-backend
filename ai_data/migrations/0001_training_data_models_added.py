# Generated by Django 3.2 on 2023-09-11 16:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImageCaptionData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('img_1_url', models.TextField(blank=True, default='')),
                ('img_1_desc', models.TextField(blank=True, default='')),
                ('img_2_url', models.TextField(blank=True, default='')),
                ('img_2_desc', models.TextField(blank=True, default='')),
                ('instruction', models.TextField(blank=True, default='')),
                ('user_rating', models.TextField(default=None, null=True)),
            ],
            options={
                'db_table': 'image_caption_data',
            },
        ),
        migrations.CreateModel(
            name='TrainingData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('video_url', models.TextField(blank=True, db_index=True, default='', null=True)),
                ('user_data', models.TextField(default=None, null=True)),
            ],
            options={
                'db_table': 'training_data',
            },
        ),
    ]