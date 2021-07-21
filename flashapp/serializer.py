from rest_framework import serializers
from .models import deck

class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = deck
        fields = ('user','name')