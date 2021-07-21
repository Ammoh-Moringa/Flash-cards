from rest_framework import serializers
from .models import *


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('profile_pic', 'bio', 'contact', 'user' )
from .models import deck

class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = deck
        fields = ('user','name')
