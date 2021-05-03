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
        fields = ['id','value_json','question','annotation', 'tweet_relation']

class ResolveTweetAnnotations_QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id','name','section','value']

class ResolveTweetAnnotations_AnswerSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    question = ResolveTweetAnnotations_QuestionSerializer()    
    value_json = serializers.ReadOnlyField()
    class Meta:
        model = Answer
        fields = ['id','value_json','question']


class ResolveTweetAnnotationsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    answers = ResolveTweetAnnotations_AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Annotation
        fields = ['id','tweet_relation','answers']
    