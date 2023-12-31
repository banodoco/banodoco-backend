from rest_framework import serializers

from user.models import User

class UserDto(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uuid', 'name', 'email', 'type', 'total_credits')

class BasicUserDto(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "uuid",
            "name",
            "email",
            "type",
            'total_credits'
        )