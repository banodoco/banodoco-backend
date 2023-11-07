# Generated by Django 3.2 on 2023-11-04 14:09

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ai_project', '0009_lock_added'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='setting',
            name='default_adapter_type',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='default_animation_style',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='default_custom_model_uuid_list',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='default_custom_pipeline',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='default_guidance_scale',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='default_high_threshold',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='default_low_threshold',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='default_negative_prompt',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='default_num_inference_steps',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='default_prompt',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='default_seed',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='default_stage',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='default_strength',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='extraction_type',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='guidance_type',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='input_video',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='rotation_angle_value',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='x_shift',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='y_shift',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='zoom_level',
        ),
        migrations.RemoveField(
            model_name='timing',
            name='adapter_type',
        ),
        migrations.RemoveField(
            model_name='timing',
            name='animation_style',
        ),
        migrations.RemoveField(
            model_name='timing',
            name='custom_model_id_list',
        ),
        migrations.RemoveField(
            model_name='timing',
            name='custom_pipeline',
        ),
        migrations.RemoveField(
            model_name='timing',
            name='frame_number',
        ),
        migrations.RemoveField(
            model_name='timing',
            name='frame_time',
        ),
        migrations.RemoveField(
            model_name='timing',
            name='guidance_scale',
        ),
        migrations.RemoveField(
            model_name='timing',
            name='high_threshold',
        ),
        migrations.RemoveField(
            model_name='timing',
            name='interpolated_clip',
        ),
        migrations.RemoveField(
            model_name='timing',
            name='interpolation_steps',
        ),
        migrations.RemoveField(
            model_name='timing',
            name='low_threshold',
        ),
        migrations.RemoveField(
            model_name='timing',
            name='negative_prompt',
        ),
        migrations.RemoveField(
            model_name='timing',
            name='num_inteference_steps',
        ),
        migrations.RemoveField(
            model_name='timing',
            name='preview_video',
        ),
        migrations.RemoveField(
            model_name='timing',
            name='project',
        ),
        migrations.RemoveField(
            model_name='timing',
            name='prompt',
        ),
        migrations.RemoveField(
            model_name='timing',
            name='seed',
        ),
        migrations.RemoveField(
            model_name='timing',
            name='strength',
        ),
        migrations.RemoveField(
            model_name='timing',
            name='timed_clip',
        ),
        migrations.RemoveField(
            model_name='timing',
            name='transformation_stage',
        ),
        migrations.CreateModel(
            name='Shot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('name', models.CharField(blank=True, default='', max_length=255)),
                ('desc', models.TextField(blank=True, default='')),
                ('shot_idx', models.IntegerField()),
                ('duration', models.FloatField(default=2.5)),
                ('meta_data', models.TextField(blank=True, default='')),
                ('interpolated_clip_list', models.TextField(default=None, null=True)),
                ('main_clip', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ai_project.internalfileobject')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ai_project.project')),
            ],
            options={
                'db_table': 'shot',
            },
        ),
        migrations.AddField(
            model_name='timing',
            name='shot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ai_project.shot'),
        ),
    ]