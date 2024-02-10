from rest_framework import serializers
from ..Product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CookieCartsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name_product', 'manya']