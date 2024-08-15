from rest_framework import serializers
from .models import ConcreteProduct


class ConcreteProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConcreteProduct
        fields = '__all__'