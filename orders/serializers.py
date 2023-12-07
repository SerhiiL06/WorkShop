from rest_framework import serializers
from .models import Order, Category
from users.models import User
from .tasks import send_email_about_new_order


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["service"]


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "category", "description", "status"]

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)

        send_email_about_new_order.delay(
            order_id=order.id,
            description=order.description,
            created=order.created,
            email=order.customer.email,
        )

        return order

    def get_category(self, obj):
        return obj.category.service

    def get_customer(self, obj):
        return obj.customer.username


class MasterOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "category", "meeting_time", "description"]


class AssignedMasterSerializer(serializers.Serializer):
    CHOISE_RESULT = (("accept", "accept"), ("rejected", "rejected"))

    master = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_master=True)
    )

    result = serializers.ChoiceField(choices=CHOISE_RESULT)
