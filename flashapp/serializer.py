from rest_framework import serializers
from .models import *

class flashCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = flashCard
        fields = ('deck', 'question', 'answer')