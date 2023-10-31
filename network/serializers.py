from rest_framework import serializers

from network.models import NetworkElement


class NetworkElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkElement
        fields = ('name', 'contacts', 'product', 'provider', 'created_at', 'level')
        read_only_fields = ('debt',)
