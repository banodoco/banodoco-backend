from rest_framework import serializers

class GoogleUserDetailsDao(serializers.Serializer):
    sub = serializers.CharField(
        required=True,
        help_text="Unique identifier for the user",
    )
    given_name = serializers.CharField(
        required=False,
        help_text="first name",
    )
    family_name = serializers.CharField(
        required=False,
        help_text="last name",
    )
    email = serializers.CharField(
        required=True,
        help_text="email",
    )
    picture = serializers.CharField(
        required=False,
        help_text="profile pic",
    )