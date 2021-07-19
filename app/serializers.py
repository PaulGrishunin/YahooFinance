from rest_framework import serializers
from .models import  Prices


class PricesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prices
        fields = ('company', 'date', 'open', 'high', 'low', 'close', 'adj_close', 'volume')


class PricesDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prices
        fields = ('date', 'open', 'high', 'low', 'close', 'adj_close', 'volume')