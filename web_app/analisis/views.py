from django.shortcuts import render
from django.http import HttpResponse
from .models import Stance, Confidence, Expressivity, Annotator, Annotation, TweetRelation


from unittest.mock import Mock
# Create your views here.


def get_tweet_relation():
    # TODO : 
    # - Get a random instance from DB 
    # - Validate tuple (AnnotatorId,TweetRelationId) to be unique in order
    #   to avoid same annotator annotate a tweet only once. Either in DB or application
    tweet_relation = Mock()
    tweet_relation.id = 1  # dummy id
    tweet_relation.tweet_source_id = 1177640691314413568
    tweet_relation.tweet_response_id = tweet_relation.tweet_source_id + 1 # dummy id
    return tweet_relation

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def quotes_simple_example(request):
    tweet_relation = get_tweet_relation()
   
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
        # tr = TweetRelation.objects.get(id=request.POST['tweet_relation_id'])

        print(a)
        print(s)
        print(c)

        # Create Annotation
        # TODO:
        # - Validate tuple (AnnotatorId,TweetRelationId) to be unique in order
        #   to avoid same annotator annotate a tweet only once. Either in DB or application
        if there_is_expressivity:
            an, created = Annotation.objects.get_or_create(
                # tweet_relation=tr,
                tweet_relation_id = tweet_relation.id,
                annotator=a,
                stance=s,
                confidence=c,
                expressivity=e
            )
        else: 
            an, created = Annotation.objects.get_or_create(
                # tweet_relation=tr,
                tweet_relation_id = tweet_relation.id,
                annotator=a,
                stance=s,
                confidence=c,
            )
        print(f'{ann}, created? = {created}')
    context = {
        'tweet_relation_id' : tweet_relation.id,
        'tweet_source_id' : tweet_relation.tweet_source_id,
        'tweet_response_id' : tweet_relation.tweet_response_id,
    }
    return render(request, 'analisis/Quotes_Simple_example.html', context = context)

def replies_simple_example(request):
    return render(request, 'analisis/Replies_Simple_example.html')
