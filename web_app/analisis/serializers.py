from rest_framework import serializers

from .models import *

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
    