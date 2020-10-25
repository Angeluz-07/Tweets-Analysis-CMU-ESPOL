from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.http.request import QueryDict
from django.http import Http404
from .models import *

from rest_framework import viewsets
from .serializers import *


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    http_method_names = ['get']

def get_random_tweet_relation(annotator_id: int) -> TweetRelation:
    # https://medium.com/better-programming/django-annotations-and-aggregations-48685994d149
    from random import choice
    from django.db.models import Count
    from .models import TweetRelation

    relation_type = choice(['Quote','Reply'])

    tr_ids_annotated_thrice = [
        item.id for item in
        TweetRelation.objects \
        .annotate(annotation_count=Count('annotation')) \
        .filter(annotation_count__gte=3)
    ]

    tr_ids_already_annotated_by_user = [
        item.id for item in
        TweetRelation.objects \
        .filter(annotation__annotator_id=annotator_id)
    ]

    trs = TweetRelation.objects \
    .filter(relation_type=relation_type) \
    .exclude(id__in=tr_ids_annotated_thrice) \
    .exclude(id__in=tr_ids_already_annotated_by_user) \
    .all()

    assert len(trs) > 0 #If not, all tweets have been annotated or DB is empty
    return choice(trs)

def get_annotation_count(annotator_id: int) -> int:
    from .models import TweetRelation
    return len(TweetRelation.objects.filter(annotation__annotator_id=annotator_id))

def create_annotation(form_data: QueryDict) -> None:  
    import json

    a = Annotator.objects.get(id=form_data['annotator_id'])
    tr = TweetRelation.objects.get(id=form_data['tweet_relation_id'])
    ts = form_data['time_spent']

    ann = Annotation.objects.create(
        tweet_relation=tr, 
        annotator=a,
        time_spent=ts
    )

    questions = {k: v for k, v in form_data.items() if k.isnumeric()}   
    for k, v in questions.items():
        q = Question.objects.get(id=k)
        if q.type == "Checkbox":
            value = json.dumps(form_data.getlist(k), ensure_ascii=False)
        else:
            value = json.dumps(v, ensure_ascii=False)
        answer = Answer.objects.create(
            value=value,
            annotation_id=ann.id,
            question_id=q.id,            
        )

def GET_random_tweet_relation(request, annotator_id):
    tweet_relation = get_random_tweet_relation(annotator_id)
    resp = {
        'id' : tweet_relation.id,
        'relation_type' : tweet_relation.relation_type,
        'tweet_target' :{
            'id' : tweet_relation.tweet_target.id,
            'text' : tweet_relation.tweet_target.text,
        },
        'tweet_response': {
            'id' : tweet_relation.tweet_response.id,
            'text' : tweet_relation.tweet_response.text,
        }
    }
    return JsonResponse(resp)

def all_tweets_available(tweet_relation):
    import requests as r
    url = 'https://syndication.twitter.com/tweet'
    tt_id = tweet_relation.tweet_target.id
    tr_id = tweet_relation.tweet_response.id
    resps = [
        r.get(f'{url}?id={tt_id}&lang=en'),
        r.get(f'{url}?id={tr_id}&lang=en')
    ]
    return all( resp.status_code==200 for resp in resps )

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def annotate(request):
    if not request.user.is_authenticated:
        return HttpResponse("User is not authenticated. Log in <a href='/login'>here</a>")

    user_id = request.user.id # User logged in
    tweet_relation = get_random_tweet_relation(user_id)

    if request.method == 'POST':
        create_annotation(request.POST)
        return redirect('annotate')
   
    context = {
        'tweet_relation_id' : tweet_relation.id,
        'tweet_target_id' : tweet_relation.tweet_target.id,
        'tweet_target_text' : tweet_relation.tweet_target.text,
        'tweet_response_id' : tweet_relation.tweet_response.id,
        'tweet_response_text' : tweet_relation.tweet_response.text,
        'relation_type' : tweet_relation.relation_type,
        'all_tweets_available' : all_tweets_available(tweet_relation),
        'annotation_count' : get_annotation_count(user_id),
    }

    return render(request, 'analisis/annotate.html', context = context)
