from django.shortcuts import render
from django.http import HttpResponse
from .models import Stance, Confidence, Expressivity, Annotator, Annotation, TweetRelation, Tweet


def get_random_tweet_relation(relation_type):
    # TODO : 
    # - Validate tuple (AnnotatorId,TweetRelationId) to be unique in order
    #   to avoid same annotator annotate a tweet only once. Either in DB or application
    # source: https://books.agiliq.com/projects/django-orm-cookbook/en/latest/random.html
    
    from django.db.models import Max
    max_id = TweetRelation.objects.filter(relation_type=relation_type).aggregate(max_id=Max("id"))['max_id']
    while True:
        from random import randint
        id = randint(1, max_id)
        tweet_relation = TweetRelation.objects.get(id=id)
        if tweet_relation:
            return tweet_relation

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def quotes_simple_example(request):
    tweet_relation = get_random_tweet_relation("Quote")
   
    if request.method == 'POST':
        there_is_expressivity = request.POST['expressivity_type'] != ''
        print(request.POST)
        
        s = Stance.objects.get(name=request.POST['stance'])
        c = Confidence.objects.get(name=request.POST['confidence'])
        if there_is_expressivity:
            e = Expressivity.objects.get(
                type=request.POST['expressivity_type'],
                value = request.POST['expressivity_value'],
                evidence = request.POST['evidence']
            )

        a = Annotator.objects.get(id=request.POST['annotator_token'])
        tr = TweetRelation.objects.get(id=request.POST['tweet_relation_id'])

        print(a)
        print(s)
        print(c)

        # Create Annotation
        # TODO:
        # - Validate tuple (AnnotatorId,TweetRelationId) to be unique in order
        #   to avoid same annotator annotate a tweet only once. Either in DB or application
        if there_is_expressivity:
            an, created = Annotation.objects.get_or_create(
                tweet_relation = tr,
                annotator=a,
                stance=s,
                confidence=c,
                expressivity=e
            )
        else: 
            an, created = Annotation.objects.get_or_create(
                tweet_relation = tr,
                annotator=a,
                stance=s,
                confidence=c,
            )
        print(f'{an}, created? = {created}')
    context = {
        'tweet_relation_id' : tweet_relation.id,
        'tweet_target_id' : tweet_relation.tweet_target_id,
        'tweet_response_id' : tweet_relation.tweet_response_id,
    }
    return render(request, 'analisis/Quotes_Simple_example.html', context = context)

def replies_simple_example(request):
    return render(request, 'analisis/Replies_Simple_example.html')
