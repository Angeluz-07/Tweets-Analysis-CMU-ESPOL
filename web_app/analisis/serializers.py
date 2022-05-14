from rest_framework import serializers

from .models import *

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Question
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    tweet_relation = serializers.ReadOnlyField()
    value_json = serializers.ReadOnlyField()
    class Meta:
        model = Answer
        fields = ['id','value','value_json','question','annotation', 'tweet_relation']

class RevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revision
        fields = ['id','tweet_relation_id','annotation_id', 'skipped']

class AppCustomConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppCustomConfig
        fields = '__all__'
