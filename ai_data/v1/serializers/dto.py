import json
from rest_framework import serializers

from ai_data.models import TrainingData

class TrainingDataDto(serializers.Serializer):
    submitted_caption_list = serializers.SerializerMethodField()
    submitted_rating_list = serializers.SerializerMethodField()

    class Meta:
        model = TrainingData
        fields = (
            'uuid',
            'video_url',
            'author_id',
            'total_caption_count',
            'total_rating_count',
            'submitted_caption_list',
            'submitted_rating_list',
            'avg_rating'
        )

    def get_submitted_caption_list(self, obj):
        return json.loads(obj.caption_list) if obj.caption_list else []
    
    def get_submitted_rating_list(self, obj):
        return json.loads(obj.rating_list) if obj.rating_list else []
    

class TrainingDataListItemDto(serializers.Serializer):
    class Meta:
        model = TrainingData
        fields = (
            'uuid',
            'video_url',
            'author_id',
            'total_caption_count',
            'total_rating_count',
            'avg_rating'
        )