from rest_framework import serializers

class UserLoginDao(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class GoogleIDTokenDao(serializers.Serializer):
    id_token = serializers.CharField(
        required=True,
        help_text="Google ID Token",
    )