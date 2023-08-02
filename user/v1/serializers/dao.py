from rest_framework import serializers

from user.constants import UserType

class CreateUserDao(serializers.Serializer):
    name = serializers.CharField()
    profile_pic_url = serializers.CharField(required=False)
    email = serializers.CharField()
    password = serializers.CharField()
    type = serializers.ChoiceField(choices=UserType.value_list(), default=UserType.USER.value)

class UpdateUserDao(serializers.Serializer):
    uuid = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    profile_pic_url = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    type = serializers.CharField(required=False)
    credits_to_add = serializers.FloatField(required=False)

class UUIDDao(serializers.Serializer):
    uuid = serializers.CharField()
    
class UserSignUpDao(serializers.Serializer):
    email = serializers.CharField(max_length=255, required=True)

class GetUserDao(serializers.Serializer):
    uuid = serializers.CharField(max_length=100, required=False)
    email = serializers.CharField(max_length=255, required=False)

class EventDao(serializers.Serializer):
    event = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(max_length=255, required=False)

class UserListFilterDao(serializers.Serializer):
    type = serializers.ChoiceField(
        choices=UserType.value_list(), required=False
    )
    page = serializers.IntegerField(default=1)
    data_per_page = serializers.IntegerField(default=20)