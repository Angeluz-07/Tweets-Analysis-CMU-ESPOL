from rest_framework import serializers

from .models import *

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Question
        fields = '__all__'
    