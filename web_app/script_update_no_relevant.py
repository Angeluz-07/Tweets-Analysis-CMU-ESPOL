import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'analisistweets.settings')

import django
django.setup()


from django.db.models import Count
from analisis.models import *
import json

#from analisis.domain import update_no_relevant
def update_no_relevant(debug):


    def get_trs_count(count):
        result = TweetRelation.objects \
        .annotate(annotation_count=Count('annotation')) \
        .filter(annotation_count__exact=count) \
        .filter(relevant=True) \
        .count()
        return result

    def get_trs(count):
        result = TweetRelation.objects \
        .annotate(annotation_count=Count('annotation')) \
        .filter(annotation_count__exact=count) \
        .filter(relevant=True) \
        .all()
        return result

    print("\tCount before update")
    for i in range(0,2+1):        
        print(f'tweets wit {i} annotations = {get_trs_count(i)}')

    ids = []
    for i in range(0,2+1):
        queryset = get_trs(i)
        ids+= queryset.values_list('id', flat=True)
    print(f'# items to save  = {len(ids)} ; {ids[:5]}...')

    import json
    outfilename = 'data/20220514_ids_marked_as_no_relevant.json'
    with open(outfilename, 'w') as outfile:
        json.dump(ids, outfile)
    print(f'saved in = {outfilename}')

    print("updating...")
    queryset = TweetRelation.objects.filter(id__in=ids).all()

    tweet_relations_to_update = []
    for tweet_relation in queryset:
        tweet_relation.relevant = False
        tweet_relations_to_update.append(tweet_relation)

    TweetRelation.objects.bulk_update(tweet_relations_to_update,['relevant'])

    print("\tCount after update")
    for i in range(0,2+1):        
        print(f'tweets wit {i} annotations = {get_trs_count(i)}')

if __name__ == '__main__':
    update_no_relevant(debug=True)
