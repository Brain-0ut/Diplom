from rest_framework import serializers
from mytrello.models import Card


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        exclude = ['created_at']
