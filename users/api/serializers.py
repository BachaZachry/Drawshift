from rest_framework import serializers
from django.contrib.auth import authenticate
from users.models import User, Invite, Team
from rest_framework.fields import CurrentUserDefault


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            # return user in case of a successful login
            return user
        # Handle wrong info
        raise serializers.ValidationError("Incorrect Credentials")


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Might be modified in case of adding another fields to the user
        fields = ["first_name", "last_name", "username", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class SocialSerializer(serializers.Serializer):
    """
    Serializer which accepts an OAuth2 access token.
    """

    access_token = serializers.CharField(allow_blank=False, trim_whitespace=True)


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class KnoxSerializer(serializers.Serializer):
    """
    Serializer for Knox authentication.
    """

    token = serializers.CharField()


class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = ["sender", "receiver", "status"]
        extra_kwargs = {"sender": {"default": CurrentUserDefault()}}


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = []
