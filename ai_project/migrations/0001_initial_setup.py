# Generated by Django 3.2 on 2023-06-29 14:39

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial_setup'),
    ]

    operations = [
        migrations.CreateModel(
            name='AIModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('name', models.CharField(default='', max_length=255)),
                ('version', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('replicate_model_id', models.CharField(blank=True, default='', max_length=255)),
                ('replicate_url', models.TextField(blank=True, default='')),
                ('diffusers_url', models.TextField(blank=True, default='')),
                ('category', models.CharField(blank=True, default='', max_length=255)),
                ('training_image_list', models.TextField(blank=True, default='')),
                ('keyword', models.CharField(blank=True, default='', max_length=255)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='user.user')),
            ],
            options={
                'db_table': 'ai_model',
            },
        ),
        migrations.CreateModel(
            name='InternalFileObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('name', models.TextField(default='')),
                ('type', models.CharField(default='', max_length=255)),
                ('local_path', models.TextField(default='')),
                ('hosted_url', models.TextField(default='')),
                ('tag', models.CharField(default='', max_length=255)),
            ],
            options={
                'db_table': 'file',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('name', models.CharField(default='', max_length=255)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='user.user')),
            ],
            options={
                'db_table': 'project',
            },
        ),
        migrations.CreateModel(
            name='Timing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('custom_model_id_list', models.TextField(blank=True, default=None, null=True)),
                ('frame_time', models.FloatField(default=None, null=True)),
                ('frame_number', models.IntegerField(default=None, null=True)),
                ('alternative_images', models.TextField(default=None, null=True)),
                ('custom_pipeline', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('prompt', models.TextField(blank=True, default='')),
                ('negative_prompt', models.TextField(blank=True, default='')),
                ('guidance_scale', models.FloatField(default=7.5)),
                ('seed', models.IntegerField(default=0)),
                ('num_inteference_steps', models.IntegerField(default=50)),
                ('strength', models.FloatField(default=4)),
                ('notes', models.TextField(blank=True, default='')),
                ('adapter_type', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('clip_duration', models.FloatField(default=None, null=True)),
                ('animation_style', models.CharField(default=None, max_length=255, null=True)),
                ('interpolation_steps', models.IntegerField(default=0)),
                ('low_threshold', models.FloatField(default=0)),
                ('high_threshold', models.FloatField(default=0)),
                ('aux_frame_index', models.IntegerField(default=0)),
                ('transformation_stage', models.CharField(default=None, max_length=255, null=True)),
                ('canny_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='canny_image', to='ai_project.internalfileobject')),
                ('interpolated_clip', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='interpolated_clip', to='ai_project.internalfileobject')),
                ('mask', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='mask', to='ai_project.internalfileobject')),
                ('model', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ai_project.aimodel')),
                ('preview_video', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='preview_video', to='ai_project.internalfileobject')),
                ('primary_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='primary_image', to='ai_project.internalfileobject')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ai_project.project')),
                ('source_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='source_image', to='ai_project.internalfileobject')),
                ('timed_clip', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='timed_clip', to='ai_project.internalfileobject')),
            ],
            options={
                'db_table': 'frame_timing',
            },
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('default_prompt', models.TextField(default='')),
                ('default_strength', models.FloatField(default=0.7)),
                ('default_custom_pipeline', models.CharField(blank=True, default='', max_length=255)),
                ('input_type', models.CharField(max_length=255)),
                ('extraction_type', models.CharField(max_length=255)),
                ('width', models.IntegerField(default=512)),
                ('height', models.IntegerField(default=512)),
                ('default_negative_prompt', models.TextField(default='')),
                ('default_guidance_scale', models.FloatField(default=7.5)),
                ('default_seed', models.IntegerField(default=0)),
                ('default_num_inference_steps', models.IntegerField(default=50)),
                ('default_stage', models.CharField(max_length=255)),
                ('default_custom_model_uuid_list', models.TextField(blank=True, default=None, null=True)),
                ('default_adapter_type', models.CharField(blank=True, default='', max_length=255)),
                ('guidance_type', models.CharField(max_length=255)),
                ('default_animation_style', models.CharField(max_length=255)),
                ('default_low_threshold', models.FloatField(default=0)),
                ('default_high_threshold', models.FloatField(default=0)),
                ('zoom_level', models.IntegerField(default=100)),
                ('x_shift', models.IntegerField(default=0)),
                ('y_shift', models.IntegerField(default=0)),
                ('rotation_angle_value', models.FloatField(default=0.0)),
                ('audio', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='audio', to='ai_project.internalfileobject')),
                ('default_model', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ai_project.aimodel')),
                ('input_video', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='input_video', to='ai_project.internalfileobject')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ai_project.project')),
            ],
            options={
                'db_table': 'setting',
            },
        ),
        migrations.AddField(
            model_name='internalfileobject',
            name='project',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ai_project.project'),
        ),
        migrations.CreateModel(
            name='InferenceLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('input_params', models.TextField(blank=True, default='')),
                ('output_details', models.TextField(blank=True, default='')),
                ('total_inference_time', models.IntegerField(default=0)),
                ('model', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ai_project.aimodel')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ai_project.project')),
            ],
            options={
                'db_table': 'inference_log',
            },
        ),
        migrations.CreateModel(
            name='BackupTiming',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('name', models.CharField(default='', max_length=255)),
                ('note', models.TextField(blank=True, default='')),
                ('data_dump', models.TextField(blank=True, default='')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ai_project.project')),
            ],
            options={
                'db_table': 'backup_timing',
            },
        ),
        migrations.CreateModel(
            name='AppSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('replicate_key', models.CharField(blank=True, default='', max_length=255)),
                ('aws_secret_access_key', models.CharField(blank=True, default='', max_length=255)),
                ('aws_access_key', models.CharField(blank=True, default='', max_length=255)),
                ('stability_key', models.CharField(blank=True, default='', max_length=255)),
                ('previous_project', models.CharField(blank=True, default='', max_length=255)),
                ('replicate_username', models.CharField(blank=True, default='', max_length=255)),
                ('welcome_state', models.IntegerField(default=0)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'db_table': 'app_setting',
            },
        ),
        migrations.CreateModel(
            name='AIModelParamMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('standard_param_key', models.CharField(blank=True, max_length=255)),
                ('model_param_key', models.CharField(blank=True, max_length=255)),
                ('model', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ai_project.aimodel')),
            ],
            options={
                'db_table': 'model_param_map',
            },
        ),
    ]