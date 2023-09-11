import json
from rest_framework import serializers

from ai_data.models import ImageCaptionData, TrainingData

class TrainingDataDto(serializers.ModelSerializer):
    user_data_list = serializers.SerializerMethodField()

    class Meta:
        model = TrainingData
        fields = (
            'uuid',
            'video_url',
            'user_data_list'
        )

    def get_user_data_list(self, obj):
        return json.loads(obj.user_data) if obj.user_data else {}
    

class TrainingDataListItemDto(serializers.ModelSerializer):
    class Meta:
        model = TrainingData
        fields = (
            'uuid',
            'video_url'
        )


class ImageCaptionDataDto(serializers.ModelSerializer):
    user_rating_list = serializers.SerializerMethodField()
    class Meta:
        model = ImageCaptionData
        fields = (
            "uuid",
            "img_1_url",
            "img_1_desc",
            "img_2_url",
            "img_2_desc",
            "instruction",
            "user_rating_list"
        )

    def get_user_rating_list(self, obj):
        return obj.user_rating_list
    

class ImageCaptionDataListItemDto(serializers.ModelSerializer):
    class Meta:
        model = ImageCaptionData
        fields = (
            "uuid",
            "img_1_url",
            "img_1_desc",
            "img_2_url",
            "img_2_desc",
            "instruction"
        )