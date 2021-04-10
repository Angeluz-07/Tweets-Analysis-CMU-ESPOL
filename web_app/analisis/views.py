from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.http.request import QueryDict
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .models import *

from rest_framework import viewsets
from .serializers import *


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    http_method_names = ['get']

def get_random_tweet_relation(annotator_id: int) -> TweetRelation:
    from random import choice
    from django.db.models import Count
    from .models import TweetRelation

    def get_trs_count(count, annotator_id):
        result = TweetRelation.objects \
        .annotate(annotation_count=Count('annotation')) \
        .filter(annotation_count__exact=count) \
        .filter(relevant=True) \
        .exclude(annotation__annotator_id=annotator_id) \
        .count()
        return result

    def get_trs(count, annotator_id):
        result = TweetRelation.objects \
        .annotate(annotation_count=Count('annotation')) \
        .filter(annotation_count__exact=count) \
        .filter(relevant=True) \
        .exclude(annotation__annotator_id=annotator_id) \
        .all()
        return result

    trs_annotated_twice_count = get_trs_count(2, annotator_id)
    trs_annotated_once_count = get_trs_count(1, annotator_id)
    trs_annotated_zero_count = get_trs_count(0, annotator_id)

    if trs_annotated_twice_count > 0:
        trs = get_trs(2, annotator_id)
    elif trs_annotated_once_count > 0:
        trs = get_trs(1, annotator_id)
    elif trs_annotated_zero_count > 0:
        trs = get_trs(0, annotator_id)
    else:
        trs = None

    return choice(trs) if trs else trs

def get_annotation_count(annotator_id: int) -> int:
    from .models import TweetRelation
    return len(TweetRelation.objects.filter(annotation__annotator_id=annotator_id))

def create_annotation(form_data: QueryDict) -> None:  
    import json

    a = Annotator.objects.get(id=form_data['annotator_id'])
    tr = TweetRelation.objects.get(id=form_data['tweet_relation_id'])
    ts = form_data['time_spent']

    anotation_on_tweet_by_user_exists =  Annotation.objects \
    .filter(tweet_relation=tr, annotator=a) \
    .exists()

    if not anotation_on_tweet_by_user_exists:
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

def hide_target_tweet(tweet_relation):
    response_tweet_is_available = all_tweets_available(tweet_relation)

    # If relation is quote, it means we only need to display the response tweet.
    # But only if the response tweet is available. Otherwise display both.
    return tweet_relation.relation_type == "Quote" and response_tweet_is_available

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@login_required(login_url='login')
def annotate(request):
    user_id = request.user.id # User logged in
    tweet_relation = get_random_tweet_relation(user_id)
    if tweet_relation is None:
        return HttpResponse("Ok. It seems all tweets have been annotated :) . Log out <a href='/logout'>here</a>")

    if request.method == 'POST':
        create_annotation(request.POST)
        return redirect('annotate')

    context = {
        'tweet_relation_id' : tweet_relation.id,
        'tweet_target_id' : tweet_relation.tweet_target.id,
        'tweet_target_text' : tweet_relation.tweet_target.text,
        'tweet_response_id' : tweet_relation.tweet_response.id,
        'tweet_response_text' : tweet_relation.tweet_response.text,
        'hide_target_tweet' : hide_target_tweet(tweet_relation),
        'annotation_count' : get_annotation_count(user_id),
    }

    return render(request, 'analisis/annotate.html', context = context)


@staff_member_required(login_url='annotate')
@login_required(login_url='login')
def resolve_tweet_annotations(request):
    context = {}
    return render(request, 'analisis/resolve_tweet_annotations.html', context = context)
