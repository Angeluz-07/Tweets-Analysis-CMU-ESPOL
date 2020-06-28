from django.shortcuts import render
from django.http import HttpResponse
from django.http.request import QueryDict
from django.http import Http404
from .models import Stance, Confidence, Expressivity, Annotator, Annotation, TweetRelation, Tweet


def get_random_tweet_relation(relation_type: str, annotator_id: int) -> TweetRelation:
    # https://medium.com/better-programming/django-annotations-and-aggregations-48685994d149
    from random import choice
    from django.db.models import Count
    from .models import TweetRelation

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
    if not request.user.is_authenticated:
        return HttpResponse("User is not authenticated. Log in <a href='/login'>here</a>")

    user_id = request.user.id # User logged in
    tweet_relation = get_random_tweet_relation(relation_type, user_id)

    if request.method == 'POST':
        create_annotation(request.POST)

    context = {
        'tweet_relation_id' : tweet_relation.id,
        'tweet_target_id' : tweet_relation.tweet_target.id,
        'tweet_target_text' : tweet_relation.tweet_target.text,
        'tweet_response_id' : tweet_relation.tweet_response.id,
        'tweet_response_text' : tweet_relation.tweet_response.text,
        'relation_type' : relation_type
    }

    return render(request, 'annotate.html', context = context)
