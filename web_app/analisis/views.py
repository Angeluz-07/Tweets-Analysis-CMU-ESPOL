from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.http.request import QueryDict
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import *

from rest_framework import viewsets
from .serializers import *


class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    http_method_names = ['get']

    @action(detail=False, methods=['GET'])
    def grouped_by_section(self, request):        
        questions = Question.objects.all().values()

        def parse_options(question):
            from json import loads
            _question = question.copy()
            _question['options'] = loads(question['options'])
            return _question

        questions = list(map(parse_options, questions))

        sections = list(dict.fromkeys(map(lambda item: item['section'],questions)))

        def build_section_info(index, section_name, questions):
            section_id = f'section_{index}'
            _questions = list(filter(lambda item: item['section']==section_name, questions))
            result = {
                'id' : section_id,
                'name': section_name,
                'questions': _questions
            }
            return result

        sections = [ build_section_info(i, section_name, questions)  for i, section_name in enumerate(sections)]
        return Response(sections)

class AnswerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    http_method_names = ['get']

    def list(self, request):
        queryset = Answer.objects.all()
        question_id = self.request.query_params.get('question.id', None)
        tweet_relation_id = self.request.query_params.get('tweet_relation.id', None)
        if question_id and tweet_relation_id:
            queryset = Answer.objects.filter(question__id=question_id, annotation__tweet_relation__id=tweet_relation_id)

        serializer = AnswerSerializer(queryset, many=True)
        return Response(serializer.data)


def add_id_to_cache(ids_type, _id):    
    from django.core.cache import cache
    cache.set(ids_type, [_id] + cache.get(ids_type, []), timeout=settings.CACHE_TIMEOUT)
    return None

def remove_id_from_cache(ids_type, input_id):
    from django.core.cache import cache
    cache.set(ids_type, [_id for _id in cache.get(ids_type, []) if _id != input_id ], timeout=settings.CACHE_TIMEOUT)
    return None

def get_ids_in_cache(ids_type):
    from django.core.cache import cache
    result = cache.get(ids_type, [])
    return result

def get_random_tweet_relation(annotator_id: int) -> TweetRelation:
    from random import choice
    from django.db.models import Count
    from .models import TweetRelation

    IN_PROGRESS_IDS = get_ids_in_cache('IN_PROGRESS_IDS')
    def get_trs_count(count, annotator_id):
        result = TweetRelation.objects \
        .annotate(annotation_count=Count('annotation')) \
        .filter(annotation_count__exact=count) \
        .filter(relevant=True) \
        .exclude(annotation__annotator_id=annotator_id) \
        .exclude(id__in=IN_PROGRESS_IDS) \
        .count()
        return result

    def get_trs(count, annotator_id):
        result = TweetRelation.objects \
        .annotate(annotation_count=Count('annotation')) \
        .filter(annotation_count__exact=count) \
        .filter(relevant=True) \
        .exclude(annotation__annotator_id=annotator_id) \
        .exclude(id__in=IN_PROGRESS_IDS) \
        .all()
        return result

    trs_annotated_twice_count = get_trs_count(2, annotator_id)
    trs_annotated_once_count = get_trs_count(1, annotator_id)
    trs_annotated_zero_count = get_trs_count(0, annotator_id)

    if trs_annotated_twice_count > 0:
        trs = get_trs(2, annotator_id)
    if trs_annotated_once_count > 0:
        trs = get_trs(1, annotator_id)
    elif trs_annotated_zero_count > 0:
        trs = get_trs(0, annotator_id)
    else:
        trs = None

    result = choice(trs) if trs else trs

    if result:
        add_id_to_cache('IN_PROGRESS_IDS', result.id)

    return result

def get_annotation_count(annotator_id: int) -> int:
    from .models import TweetRelation
    return len(TweetRelation.objects.filter(annotation__annotator_id=annotator_id))

def create_annotation(form_data: QueryDict):  
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

        remove_id_from_cache('IN_PROGRESS_IDS', tr.id)

        return ann
    return None

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

def create_revision(skipped, tweet_relation_id, annotation):    
    from .models import Revision
    result = Revision.objects.create(
        tweet_relation_id=tweet_relation_id,
        annotation=annotation,
        skipped = skipped
    )
    return result

@login_required(login_url='login')
@permission_required('analisis.view_tweetrelation',login_url='login')
def resolve_tweet_relation(request, tweet_relation_id):
    from .models import TweetRelation, Revision
    tweet_relation = get_object_or_404(TweetRelation.objects, id=tweet_relation_id)

    # Validate if is problematic before return
    if not tweet_relation.is_problematic:
        return redirect('problematic_tweet_relations')

    if request.method == 'POST':
        skipped = 'skipped' in request.POST
        if not tweet_relation.has_revision and skipped:
            create_revision(skipped,tweet_relation_id, annotation=None)            
        elif not tweet_relation.has_revision and not skipped:
            annotation = create_annotation(request.POST)
            create_revision(skipped, tweet_relation_id, annotation=annotation)            
        elif tweet_relation.has_revision and not skipped:
            annotation = create_annotation(request.POST)
            revision = Revision.objects.get(tweet_relation_id=tweet_relation_id)
            revision.annotation = annotation
            revision.save()

        remove_id_from_cache('RESOLVE_TWEET_RELATION', tweet_relation_id)
        return redirect('problematic_tweet_relations')

    if tweet_relation_id in get_ids_in_cache('RESOLVE_TWEET_RELATION'):
        return render(request, 'analisis/taken_tweet_relation.html')

    add_id_to_cache('RESOLVE_TWEET_RELATION', tweet_relation_id)

    context = {
        'tweet_relation_id' : tweet_relation.id,
        'tweet_target_id' : tweet_relation.tweet_target.id,
        'tweet_target_text' : tweet_relation.tweet_target.text,
        'tweet_response_id' : tweet_relation.tweet_response.id,
        'tweet_response_text' : tweet_relation.tweet_response.text,
        'hide_target_tweet' : hide_target_tweet(tweet_relation),
        'is_skipped' : tweet_relation.is_skipped,
    }

    return render(request, 'analisis/resolve_tweet_relation.html', context = context)


def get_problematic_tweet_relations():    
    from django.db.models import Count

    IN_PROGRESS_IDS = get_ids_in_cache('RESOLVE_TWEET_RELATION')
    queryset = TweetRelation.objects \
        .filter(relevant=True) \
        .exclude(id__in=IN_PROGRESS_IDS) \
        .annotate(annotation_count=Count('annotation')) \
        .filter(annotation_count__exact=3) \
        .prefetch_related(      
            'annotation_set__answers',
            'revision',
        ) \
        .only('id')[:100]

    result = [ 
        item for item in queryset
        if item.is_problematic and not item.is_resolved
    ]
    return result

@login_required(login_url='login')
@permission_required('analisis.view_tweetrelation',login_url='login')
def problematic_tweet_relations(request):
    trs = get_problematic_tweet_relations()

    context = {
        'trs' : trs
    }
    return render(request, 'analisis/problematic_tweet_relations.html', context = context)


@login_required(login_url='login')
@permission_required('analisis.view_tweetrelation',login_url='login')
def all_annotations_count(request):
    
    from django.db.models import Count
    from .models import TweetRelation
    def get_trs_count(count):
        result = TweetRelation.objects \
        .filter(relevant=True) \
        .annotate(annotation_count=Count('annotation')) \
        .filter(annotation_count__exact=count) \
        .count()
        return result
    
    context = {
        'zero' : get_trs_count(0),
        'one' : get_trs_count(1),
        'two' : get_trs_count(2),
        'three': get_trs_count(3),
        'four': get_trs_count(4), 
        'five': get_trs_count(5) 
    }
    return render(request, 'analisis/all_annotations_count.html', context = context)

