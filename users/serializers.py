from .models import User
import re
from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    def create(self, validated_data):
        user = User.objects.create(username=validated_data["username"])

        user.set_password(validated_data["password1"])

        user.save()

        return user

    def validate_password1(self, value):
        result = re.findall(r"['A-Za-z0-9']{8,}", value)
        if not result:
            raise serializers.ValidationError(detail="wrond regex")
        return value


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "is_staff", "is_master"]
