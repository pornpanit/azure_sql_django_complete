from rest_framework import serializers
from .models import Store, Product, Order, OrderItem
from django.contrib.auth.models import User


class StoreSerializer(serializers.ModelSerializer):
    # Serializer for Store model
    class Meta:
        model = Store
        fields = ['store_id', 'store_location']


class ProductSerializer(serializers.ModelSerializer):
    # Serializer for Product model
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False
    )
    class Meta:
        model = Product
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    # Serializer for User model
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class OrderItemSerializer(serializers.ModelSerializer):
    # Serializer for OrderItem model
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.DecimalField(
        source='product.price',
        max_digits=10,
        decimal_places=2,
        read_only=True,
        coerce_to_string=False
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    # Serializer for Order model
    items = OrderItemSerializer(many=True)
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'created_at', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
