from rest_framework import serializers
<<<<<<< HEAD
from .models import *


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('profile_pic', 'bio', 'contact', 'user' )
=======
from .models import deck

class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = deck
        fields = ('user','name')
>>>>>>> 18de43d0b432db371a13b9a1020d02b5f2bf5000
