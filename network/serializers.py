from rest_framework import serializers

from network.models import NetworkElement


class NetworkElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkElement
        fields = ('name', 'contacts', 'product', 'provider', 'debt', 'created_at', 'level',)
        read_only_fields = ('debt',)

    def set_level(self, validated_data):
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
        self.set_level(validated_data)
        instance = NetworkElement.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
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
        provider = data.get('provider')
        level = data.get('level')
        if provider and provider.level is not None:
            if level == '0':
                raise serializers.ValidationError("У 0 уровня не может быть поставщика")
            elif provider.level > level:
                raise serializers.ValidationError("Поставщик должен быть предыдущим по иерархии звеном.")
        else:
            if level != '0':
                raise serializers.ValidationError("Только у завода не может быть поставщика.")

        return data
