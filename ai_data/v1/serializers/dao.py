from rest_framework import serializers

class TrainingDataDao(serializers.Serializer):
    uuid = serializers.CharField(max_length=100, allow_blank=True, allow_null=True, required=False)
    video_url = serializers.CharField(max_length=None, allow_blank=True, allow_null=True, required=False)

    def validate(self, data):
        uuid = data.get("uuid")
        video_url = data.get("video_url")

        if not uuid and not video_url:
            raise serializers.ValidationError(
                "At least one of uuid or video_url is required."
            )

        return data

class CreateTrainingDataDao(serializers.Serializer):
    video_url = serializers.CharField(max_length=None)
    

class UpdateTrainingDataDao(serializers.Serializer):
    uuid = serializers.CharField(max_length=100, allow_blank=True, allow_null=True, required=False)
    video_url = serializers.CharField(max_length=None, allow_blank=True, allow_null=True, required=False)
    start_idx = serializers.IntegerField()
    end_idx = serializers.IntegerField()
    caption = serializers.CharField(max_length=None, allow_blank=True, allow_null=True, required=False)
    rating = serializers.IntegerField(required=False)

    def validate(self, data):
        uuid = data.get("uuid")
        video_url = data.get("video_url")

        if not uuid and not video_url:
            raise serializers.ValidationError(
                "At least one of uuid or video_url is required."
            )

        return data
    

class TrainingDataFilterDao(serializers.Serializer):
    page = serializers.IntegerField(default=1)
    data_per_page = serializers.IntegerField(default=100)


class CaptionDataListFilterDao(serializers.Serializer):
    page = serializers.IntegerField(default=1)
    data_per_page = serializers.IntegerField(default=100)


class UUIDDao(serializers.Serializer):
    uuid = serializers.CharField(max_length=100)


class CreateImageCaptionDataDao(serializers.Serializer):
    img_1_url = serializers.CharField(max_length=None)
    img_1_desc = serializers.CharField(max_length=None)
    img_2_url = serializers.CharField(max_length=None)
    img_2_desc = serializers.CharField(max_length=None)
    instruction = serializers.CharField(max_length=None, default="")


class UpdateImageCaptionDataDao(serializers.Serializer):
    uuid = serializers.CharField(max_length=100)
    img_1_url = serializers.CharField(max_length=None, required=False)
    img_1_desc = serializers.CharField(max_length=None, required=False)
    img_2_url = serializers.CharField(max_length=None, required=False)
    img_2_desc = serializers.CharField(max_length=None, required=False)
    instruction = serializers.CharField(max_length=None, default="", required=False)
    user_rating = serializers.IntegerField(required=False)