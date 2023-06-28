from rest_framework import serializers

from user.models import User

class UserDto(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uuid', 'name', 'email', 'profile_pic_url', 'type')

class BasicUserDto(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "uuid",
            "name",
            "email",
            "type"
        )