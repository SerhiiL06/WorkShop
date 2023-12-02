from rest_framework import serializers
from .models import Order, Category
from users.models import User
from users.serializers import UserReadSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["service"]


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["category", "description"]

    def get_category(self, obj):
        return obj.category.service

    def get_customer(self, obj):
        return obj.customer.username


class AssignedMasterSerializer(serializers.Serializer):
    CHOISE_RESULT = (("accept", "accept"), ("rejected", "rejected"))

    master = serializers.ChoiceField(choices=User.objects.filter(is_master=True))

    result = serializers.ChoiceField(choices=CHOISE_RESULT)
