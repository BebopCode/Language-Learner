from rest_framework import serializers
from .models import WordModel

class WordModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordModel
        fields = ['id', 'word', 'meaning']

        