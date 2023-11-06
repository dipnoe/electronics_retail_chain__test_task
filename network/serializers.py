from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from network.models import NetworkElement, Product, Contact


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class NetworkElementSerializer(serializers.ModelSerializer):
    """ Serializer for the NetworkElement model. """
    products = ProductSerializer(many=True, read_only=True)
    products_ids = serializers.ListField(
        write_only=True,
        child=serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=False)
    )
    contacts = ContactSerializer(read_only=False, many=False)

    class Meta:
        model = NetworkElement
        fields = ('name', 'contacts', 'provider', 'products', 'debt', 'created_at', 'level', 'products_ids',)
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
        products = validated_data.pop('products_ids')
        contacts = validated_data.pop('contacts')
        contacts_instance = Contact.objects.create(**contacts)
        instance = NetworkElement.objects.create(**validated_data, contacts=contacts_instance)
        instance.products.set(products)

        return instance

    def update(self, instance, validated_data):
        """ Update an existing NetworkElement instance with validated data. """
        try:
            self.set_level(validated_data)
        except serializers.ValidationError as e:
            raise e
        else:
            try:
                contact = get_object_or_404(Contact, pk=instance.contacts.pk)
                contacts_update = validated_data.pop('contacts')
                for attr, value in contacts_update.items():
                    setattr(contact, attr, value)
                contact.save()
            except KeyError as k:
                print(k)
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            try:
                products = validated_data.pop('products_ids')
                instance.products.set(products)
            except KeyError as k:
                print(k)
        finally:
            instance.save()

        return instance

    def validate(self, data):
        """ Validate the 'provider' and 'level' relationships. """
        provider = data.get('provider')
        level = data.get('level')
        products_ids = data.get('products_ids')
        if provider and level:
            if level == '0':
                raise serializers.ValidationError("У 0 уровня не может быть поставщика")
            elif provider.level < level:
                raise serializers.ValidationError("Поставщик должен быть предыдущим по иерархии звеном.")

        return data
