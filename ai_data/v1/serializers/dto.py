import json
from rest_framework import serializers

from ai_data.models import TrainingData

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