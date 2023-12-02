from rest_framework import serializers
from .models import Order, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["service"]


class OrderSerializer(serializers.ModelSerializer):
    # category = serializers.ChoiceField(Category.service)
    customer = serializers.IntegerField(read_only=True)

    class Meta:
        model = Order
        fields = ["category", "description", "customer"]
