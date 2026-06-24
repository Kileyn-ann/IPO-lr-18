from rest_framework import serializers
from .models import *
from .models import Product, Category, Manufacturer, CartItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'all'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'all'


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = 'all'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = 'all'
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
