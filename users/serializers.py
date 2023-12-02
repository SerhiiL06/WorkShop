from .models import User
from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    def create(self, validated_data):
        if validated_data["password1"] != validated_data["password2"]:
            raise ValueError("Password must be similar")

        user = User.objects.create(username=validated_data["username"])

        user.set_password(validated_data["password1"])

        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "is_staff", "is_master"]
