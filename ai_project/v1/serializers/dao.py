from argparse import FileType
from rest_framework import serializers

from ai_project.constants import (
    AIModelType,
    AnimationStyleType,
    GuidanceType,
    InternalFileType,
)


class UUIDDao(serializers.Serializer):
    uuid = serializers.CharField(max_length=100)

class OptionalUUIDDao(serializers.Serializer):
    uuid = serializers.CharField(max_length=100, required=False)

class CreateUserDao(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=100)
    type = serializers.CharField(max_length=100, default="user")
    third_party_id = serializers.CharField(max_length=100, default=None, required=False)


############### FILE #################
class FileUUIDListDao(serializers.Serializer):
    uuid_list = serializers.ListField(child=serializers.CharField(max_length=100))
    
class CreateFileDao(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    type = serializers.ChoiceField(choices=InternalFileType.value_list())
    local_path = serializers.CharField(max_length=512, required=False)
    hosted_url = serializers.CharField(max_length=512)
    tag = serializers.CharField(max_length=100, required=False)
    project_id = serializers.CharField(max_length=100, required=False)

    def validate(self, data):
        local_path = data.get("local_path")
        hosted_url = data.get("hosted_url")

        if not local_path and not hosted_url:
            raise serializers.ValidationError(
                "At least one of local_path or hosted_url is required."
            )

        return data

class UploadFileDao(serializers.Serializer):
    file = serializers.FileField(allow_empty_file=True)
    extension = serializers.CharField(default="", required=False)
    type = serializers.CharField(default='general_pics')
    optimize = serializers.BooleanField(default=False)

class UpdateFileDao(serializers.Serializer):
    uuid = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100, required=False)
    type = serializers.ChoiceField(
        choices=InternalFileType.value_list(), required=False
    )
    local_path = serializers.CharField(max_length=512, required=False)
    hosted_url = serializers.CharField(max_length=512, required=False)
    tag = serializers.CharField(max_length=100, required=False)
    project_id = serializers.CharField(max_length=100, required=False)


class FileListFilterDao(serializers.Serializer):
    project_id = serializers.CharField(max_length=100, required=False)
    type = serializers.ChoiceField(
        choices=InternalFileType.value_list(), required=False
    )
    tag = serializers.CharField(max_length=100, required=False)
    page = serializers.IntegerField(default=1)
    data_per_page = serializers.IntegerField(default=100)


################# PROJECT #############
class CreateProjectDao(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    user_id = serializers.CharField(max_length=100, required=False)
    temp_file_list = serializers.CharField(max_length=None, required=False)


class UpdateProjectDao(serializers.Serializer):
    uuid = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100, required=False)
    temp_file_list = serializers.CharField(max_length=None, required=False)


class ProjectFilterDao(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=False)
    page = serializers.IntegerField(default=1)
    data_per_page = serializers.IntegerField(default=100)


################ AI MODEL ###############
class CreateAIModelDao(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    user_id = serializers.CharField(max_length=100, required=False)
    custom_trained = serializers.BooleanField(default=False, required=False)
    version = serializers.CharField(max_length=100, allow_null=True, required=False)
    replicate_url = serializers.CharField(max_length=512, default="", allow_blank=True, required=False)
    diffusers_url = serializers.CharField(max_length=512, default="", allow_blank=True, required=False)
    training_image_list = serializers.CharField(max_length=None, default="", allow_blank=True, required=False)
    category = serializers.ChoiceField(choices=AIModelType.value_list())
    keyword = serializers.CharField(
        max_length=255, default="", allow_blank=True, required=False
    )
    model_type = serializers.CharField(max_length=None)


class UpdateAIModelDao(serializers.Serializer):
    uuid = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100, required=False)
    custom_trained = serializers.BooleanField(required=False)
    user_id = serializers.CharField(max_length=100, required=False)
    version = serializers.CharField(max_length=100, required=False)
    replicate_url = serializers.CharField(max_length=512, default="", required=False)
    diffusers_url = serializers.CharField(max_length=512, default="", required=False)
    training_image_list = serializers.CharField(max_length=None, allow_blank=True, required=False)
    category = serializers.ChoiceField(choices=AIModelType.value_list(), required=False)
    keyword = serializers.CharField(max_length=255, required=False)
    model_type = serializers.CharField(max_length=None, required=False)


class AIModelListFilterDao(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=False)
    custom_trained = serializers.ChoiceField(default="all", choices=["user", "predefined", "all"], required=False)
    page = serializers.IntegerField(default=1)
    model_type_list = serializers.ListField(child=serializers.CharField(max_length=100), required=False)
    model_category_list = serializers.ListField(child=serializers.CharField(max_length=100), required=False)
    data_per_page = serializers.IntegerField(default=100)


############### INFERENCE LOG ###############
class CreateInferenceLogDao(serializers.Serializer):
    project_id = serializers.CharField(max_length=100, required=False)
    model_id = serializers.CharField(max_length=100, required=False)
    input_params = serializers.CharField(required=False)
    output_details = serializers.CharField(required=False)
    total_inference_time = serializers.CharField(required=False)

class UpdateInferenceLogDao(serializers.Serializer):
    uuid = serializers.CharField(max_length=100)
    project_id = serializers.CharField(max_length=100, required=False)
    model_id = serializers.CharField(max_length=100, required=False)
    input_params = serializers.CharField(required=False)
    output_details = serializers.CharField(required=False)
    total_inference_time = serializers.CharField(required=False)

class InferenceLogListFilterDao(serializers.Serializer):
    project_id = serializers.CharField(max_length=100, required=False)
    model_id = serializers.CharField(max_length=100, required=False)
    page = serializers.IntegerField(default=1)
    data_per_page = serializers.IntegerField(default=100)


################ PARAM MAP ###############
class CreateAIModelParamMapDao(serializers.Serializer):
    model_id = serializers.CharField(max_length=100)
    standard_param_key = serializers.CharField(max_length=100, required=False)
    model_param_key = serializers.CharField(max_length=100, required=False)


################ FRAME TIMING ###############
class CreateTimingDao(serializers.Serializer):
    project_id = serializers.CharField(max_length=100)
    model_id = serializers.CharField(max_length=100, required=False)
    source_image_id = serializers.CharField(max_length=100, required=False)
    interpolated_clip_id = serializers.CharField(max_length=100, required=False)
    timed_clip_id = serializers.CharField(max_length=100, required=False)
    mask_id = serializers.CharField(max_length=100, required=False)
    canny_image_id = serializers.CharField(max_length=100, required=False)
    preview_video_id = serializers.CharField(max_length=100, required=False)
    custom_model_id_list = serializers.CharField(max_length=100, required=False)
    frame_time = serializers.CharField(max_length=100)
    frame_number = serializers.CharField(max_length=100, required=False)
    primary_image_id = serializers.CharField(max_length=100, required=False)
    alternative_images = serializers.CharField(max_length=100, required=False)
    custom_pipeline = serializers.CharField(max_length=100, required=False)
    prompt = serializers.CharField(max_length=1024, required=False)
    negative_prompt = serializers.CharField(max_length=1024, required=False)
    guidance_scale = serializers.FloatField(required=False)
    seed = serializers.IntegerField(required=False)
    num_inteference_steps = serializers.IntegerField(required=False)
    strength = serializers.FloatField(required=False)
    notes = serializers.CharField(max_length=1024, required=False)
    adapter_type = serializers.CharField(max_length=255, required=False)
    clip_duration = serializers.FloatField(default=0, required=False)
    animation_style = serializers.CharField(
        max_length=100, default=AnimationStyleType.INTERPOLATION.value, required=False
    )
    interpolation_steps = serializers.IntegerField(required=False)
    low_threshold = serializers.FloatField(default=0, required=False)
    high_threshold = serializers.FloatField(default=0, required=False)
    aux_frame_index = serializers.IntegerField(required=False)

class UpdateTimingDao(serializers.Serializer):
    uuid = serializers.CharField(max_length=100)
    model_id = serializers.CharField(max_length=100, required=False)
    source_image_id = serializers.CharField(max_length=100, allow_null=True, required=False)
    interpolated_clip_id = serializers.CharField(max_length=100, allow_null=True, required=False)
    timed_clip_id = serializers.CharField(max_length=100, allow_null=True, required=False)
    mask_id = serializers.CharField(max_length=100, allow_null=True, required=False)
    canny_image_id = serializers.CharField(max_length=100, allow_null=True, required=False)
    preview_video_id = serializers.CharField(max_length=100, allow_null=True, required=False)
    custom_model_id_list = serializers.CharField(max_length=100, allow_null=True, required=False)
    frame_time = serializers.CharField(max_length=100, required=False)
    frame_number = serializers.CharField(max_length=100, required=False)
    primary_image_id = serializers.CharField(max_length=100, allow_null=True, required=False)
    alternative_images = serializers.CharField(max_length=None, allow_null=True, required=False)
    custom_pipeline = serializers.CharField(max_length=255, allow_null=True, required=False)
    prompt = serializers.CharField(max_length=1024, allow_blank=True, required=False)
    negative_prompt = serializers.CharField(max_length=1024, allow_blank=True, required=False)
    guidance_scale = serializers.FloatField(required=False)
    seed = serializers.IntegerField(required=False)
    num_inteference_steps = serializers.IntegerField(required=False)
    strength = serializers.FloatField(required=False)
    notes = serializers.CharField(max_length=1024, required=False)
    adapter_type = serializers.CharField(max_length=255, allow_null=True, required=False)
    clip_duration = serializers.FloatField(allow_null=True, required=False)
    animation_style = serializers.CharField(
        max_length=100, allow_null=True, required=False
    )
    interpolation_steps = serializers.IntegerField(required=False)
    low_threshold = serializers.FloatField(required=False)
    high_threshold = serializers.FloatField(required=False)
    aux_frame_index = serializers.IntegerField(required=False)
    transformation_stage = serializers.CharField(allow_null=True, required=False)

class GetProjectTimingDao(serializers.Serializer):
    project_id = serializers.CharField(max_length=100)
    frame_number = serializers.IntegerField()

class GetTimingNumberDao(serializers.Serializer):
    uuid = serializers.CharField(max_length=100)
    distance = serializers.IntegerField()

class TimingListFilterDao(serializers.Serializer):
    project_id = serializers.CharField(max_length=100)
    page = serializers.IntegerField(default=1)
    data_per_page = serializers.IntegerField(default=100)

class ShiftTimingDao(serializers.Serializer):
    project_id = serializers.CharField(max_length=100)
    index_of_frame = serializers.IntegerField()

class CreateAppSettingDao(serializers.Serializer):
    user_id = serializers.CharField(max_length=100, required=False)
    replicate_key = serializers.CharField(max_length=100, default="", required=False)
    aws_access_key = serializers.CharField(max_length=100, required=False)
    previous_project = serializers.CharField(max_length=100, required=False)
    replicate_username = serializers.CharField(
        max_length=100, default="", required=False
    )
    welcome_state = serializers.IntegerField(default=0, required=False)


class UpdateAppSettingDao(serializers.Serializer):
    uuid = serializers.CharField(max_length=100, required=False)
    user_id = serializers.CharField(max_length=100, required=False)
    replicate_key = serializers.CharField(max_length=100, required=False)
    aws_access_key = serializers.CharField(max_length=100, required=False)
    previous_project = serializers.CharField(max_length=100, required=False)
    replicate_username = serializers.CharField(max_length=100, required=False)
    welcome_state = serializers.IntegerField(default=0, required=False)


class CreateSettingDao(serializers.Serializer):
    project_id = serializers.CharField(max_length=255)
    default_model_id = serializers.CharField(max_length=255, required=False)
    audio_id = serializers.CharField(max_length=255, required=False)
    input_video_id = serializers.CharField(max_length=255, required=False)
    default_prompt = serializers.CharField(max_length=255, required=False)
    default_strength = serializers.FloatField(default=0.63, required=False)
    default_custom_pipeline = serializers.CharField(
        max_length=255, default="", allow_blank=True, required=False
    )
    input_type = serializers.CharField(max_length=255, required=False)
    extraction_type = serializers.CharField(max_length=255, required=False)
    width = serializers.IntegerField(default=512, required=False)
    height = serializers.IntegerField(default=512, required=False)
    default_negative_prompt = serializers.CharField(
        max_length=1024, default="", allow_blank=True, required=False
    )
    default_guidance_scale = serializers.FloatField(default=7.5, required=False)
    default_seed = serializers.IntegerField(default=255512, required=False)
    default_num_inference_steps = serializers.IntegerField(default=40, required=False)
    default_stage = serializers.CharField(max_length=255)
    default_custom_model_uuid_list = serializers.CharField(
        default="[]", max_length=1024, required=False
    )
    default_adapter_type = serializers.CharField(
        default="", max_length=255, required=False
    )
    guidance_type = serializers.CharField(
        default=GuidanceType.IMAGE.value, max_length=255, required=False
    )
    default_animation_style = serializers.CharField(
        default="", max_length=255, required=False
    )
    default_low_threshold = serializers.IntegerField(default=0, required=False)
    default_high_threshold = serializers.IntegerField(default=100, required=False)


class UpdateSettingDao(serializers.Serializer):
    project_id = serializers.CharField(max_length=255)
    default_model_id = serializers.CharField(max_length=255, required=False)
    audio_id = serializers.CharField(max_length=255, required=False)
    input_video_id = serializers.CharField(max_length=255, required=False)
    default_prompt = serializers.CharField(max_length=255, required=False)
    default_strength = serializers.CharField(max_length=255, required=False)
    default_custom_pipeline = serializers.CharField(max_length=255, required=False)
    input_type = serializers.CharField(max_length=255, required=False)
    extraction_type = serializers.CharField(max_length=255, required=False)
    width = serializers.IntegerField(required=False)
    height = serializers.IntegerField(required=False)
    default_negative_prompt = serializers.CharField(
        max_length=1024, default="", allow_blank=True, required=False
    )
    default_guidance_scale = serializers.FloatField(required=False)
    default_seed = serializers.IntegerField(required=False)
    default_num_inference_steps = serializers.IntegerField(required=False)
    default_stage = serializers.CharField(max_length=255, required=False)
    default_custom_model_id_list = serializers.CharField(
        max_length=1024, required=False
    )
    default_adapter_type = serializers.CharField(max_length=255, required=False)
    guidance_type = serializers.CharField(max_length=255, required=False)
    default_animation_style = serializers.CharField(max_length=255, required=False)
    default_low_threshold = serializers.IntegerField(required=False)
    default_high_threshold = serializers.IntegerField(required=False)
