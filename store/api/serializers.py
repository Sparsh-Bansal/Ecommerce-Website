from store.models import Product , OrderItem , ShippingAddress , FullOrder , Purchased_item
from store.models import ProductCategories
from rest_framework import serializers


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategories
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullOrder
        fields = '__all__'


class ShippingAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShippingAddress
        exclude = ['user']

    def create(self, validated_data):
        return ShippingAddress.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.recepient_fullname = validated_data.get('recepient_fullname', instance.recepient_fullname)
        instance.phone_no = validated_data.get('phone_no', instance.phone_no)
        instance.address_line1 = validated_data.get('address_line1', instance.address_line1)
        instance.address_line2 = validated_data.get('address_line2', instance.address_line2)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.country = validated_data.get('country', instance.country)
        instance.zipcode = validated_data.get('zipcode', instance.zipcode)
        instance.save()
        return instance

