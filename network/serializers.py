from rest_framework import serializers
from network.models import NetworkElement, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class NetworkElementSerializer(serializers.ModelSerializer):
    """ Serializer for the NetworkElement model. """
    # products = serializers.ListField(
    #     child=serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=False))
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = NetworkElement
        fields = ('name', 'contacts', 'provider', 'products', 'debt', 'created_at', 'level',)
        read_only_fields = ('debt', 'level',)

    def set_level(self, validated_data):
        """ Set the 'level' field based on the 'provider' field. """
        provider = validated_data.get('provider')
        level = self.data.get('level') if provider else '0'

        if provider:
            if provider.level == '0':
                level = '1'
            elif provider.level == '1':
                level = '2'
            else:
                raise serializers.ValidationError(f"Нельзя выбрать {provider.name} поставщиком.")

        validated_data['level'] = level

    def create(self, validated_data):
        """ Create a new NetworkElement instance with validated data. """
        self.set_level(validated_data)
        product_instances = validated_data.pop('products')
        instance = NetworkElement.objects.create(**validated_data)
        products_ = Product.objects.all()
        # for product in products_:
        #     print(product.pk)
            # if products_.get(pk=product.pk):
            #     instance.products.set(product)

        return instance

    def update(self, instance, validated_data):
        """ Update an existing NetworkElement instance with validated data. """
        try:
            self.set_level(validated_data)
        except serializers.ValidationError as e:
            raise e
        else:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.save()

            return instance

    def validate(self, data):
        """ Validate the 'provider' and 'level' relationships. """
        provider = data.get('provider')
        level = data.get('level')
        if provider and level:
            if level == '0':
                raise serializers.ValidationError("У 0 уровня не может быть поставщика")
            elif provider.level < level:
                raise serializers.ValidationError("Поставщик должен быть предыдущим по иерархии звеном.")

        return data
