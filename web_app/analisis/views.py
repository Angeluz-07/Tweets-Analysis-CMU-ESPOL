from django.shortcuts import render
from django.http import HttpResponse
from django.http.request import QueryDict
from django.http import Http404
from django.db.models import Count

from .models import Stance, Confidence, Expressivity, Annotator, Annotation, TweetRelation, Tweet


def get_random_tweet_relation(relation_type: str) -> TweetRelation:
    # Ids of TweetRelation annotated more than 3 times
    # https://medium.com/better-programming/django-annotations-and-aggregations-48685994d149
    tr_ids_black_list = [
        item.id for item in
        TweetRelation.objects \
        .annotate(annotation_count=Count('annotation')) \
        .filter(annotation_count__gte=3)
    ]

    # TODO : 
    # - Validate tuple (AnnotatorId,TweetRelationId) to be unique in order
    #   to avoid same annotator annotate a tweet only once. Either in DB or application
    # https://books.agiliq.com/projects/django-orm-cookbook/en/latest/random.html
    
    from django.db.models import Max
    max_id = TweetRelation.objects.filter(relation_type=relation_type).aggregate(max_id=Max("id"))['max_id']
    while True:
        from random import randint
        id = randint(1, max_id)

        tweet_relation = TweetRelation.objects \
        .exclude(id__in=tr_ids_black_list) \
        .filter(relation_type=relation_type) \
        .filter(id=id) \
        .first()

        if tweet_relation:
            return tweet_relation

def create_annotation(form_data: QueryDict) -> None:
    s = Stance.objects.get(name=form_data['stance'])
    c = Confidence.objects.get(name=form_data['confidence'])
    a = Annotator.objects.get(id=form_data['annotator_id'])
    tr = TweetRelation.objects.get(id=form_data['tweet_relation_id'])

    there_is_expressivity = form_data['expressivity_type'] != ''
    if there_is_expressivity:
        e = Expressivity.objects.get(
            type=form_data['expressivity_type'],
            value=form_data['expressivity_value'],
            evidence=form_data['evidence']
        )
    else:
        e = None

    # Create Annotation
    # TODO:
    # - Validate tuple (AnnotatorId,TweetRelationId) to be unique in order
    #   to avoid same annotator annotate a tweet only once. Either in DB or application
    an, created = Annotation.objects.get_or_create(
        tweet_relation = tr,
        annotator=a,
        stance=s,
        confidence=c,
        expressivity=e
    )
    print(f'{an}, created? = {created}')


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def annotate(request, relation_type: str):
    if relation_type not in ['Quote','Reply']:
        raise Http404()

    tweet_relation = get_random_tweet_relation(relation_type)

    if request.method == 'POST':
        create_annotation(request.POST)
        
    context = {
        'tweet_relation_id' : tweet_relation.id,
        'tweet_target_id' : tweet_relation.tweet_target_id,
        'tweet_response_id' : tweet_relation.tweet_response_id,
        'relation_type' : relation_type
    }

    return render(request, 'annotate.html', context = context)
