import pandas as pd

QUESTION_IDS_OF_INTEREST = [2,3,4,5,6,7,9,10]

def get_answers(tweet_relation):
    for annotation in tweet_relation.annotation_set.all():
        for answer in annotation.answers.all():
            yield {
                #'annotation_id': annotation.id,
                'question_id': answer.question_id,
                #'answer_id': answer.id,
                'value': answer.value
            }

def has_inconsistent_answers(series):
    result = series.value_counts()/len(series)
    return ( result <= 0.5 ).all()

def has_enough_answers(series):
    return len(series) == 3

def is_problematic(series):
    return has_enough_answers(series) and has_inconsistent_answers(series)

def tweet_relation_is_problematic(tweet_relation):
    df = pd.DataFrame().from_records(list(get_answers(tweet_relation)))
    
    questions_of_interest = df['question_id'].isin(QUESTION_IDS_OF_INTEREST)
    df = df[questions_of_interest]
    
    aggregated = df.sort_values('question_id').groupby('question_id').agg({'value':[is_problematic]})

    return aggregated[('value','is_problematic')].any()

def update_problematics(debug=False):    
    from django.db.models import Count
    from .models import TweetRelation

    queryset = TweetRelation.objects \
        .filter(relevant=True) \
        .annotate(annotation_count=Count('annotation')) \
        .filter(annotation_count__exact=3) \
        .prefetch_related('annotation_set__answers') \
        .all()
    
    total_items = queryset.count()

    if debug:
        from datetime import datetime
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print('Starting <update problematics> job at :', dt_string)

    STEP = 2000
    for i in range(0, total_items, STEP):
        _slice = queryset[i:i+STEP]

        tweet_relations_to_update = []
        for tweet_relation in _slice:
            if tweet_relation_is_problematic(tweet_relation):
                tweet_relation.problematic = True
                tweet_relations_to_update.append(tweet_relation)

        if debug:
            print('to update, n items = ', len(tweet_relations_to_update))

        TweetRelation.objects.bulk_update(tweet_relations_to_update,['problematic'])
    

    if debug:
        from datetime import datetime
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print('Finishing <update problematics> job at :', dt_string)
        print()

    return None

def get_preselected_tweet_relations_ids():
    import os
    BASE_DIR = os.path.dirname(os.path.abspath("__file__"))
    path = os.path.join(BASE_DIR, 'data', 'annotations_to_revise.csv')

    import csv
    if os.path.exists(path):
        with open(path, 'r') as file:
            reader = csv.DictReader(file)
            result = list(set([int(row["tweet_relation_id"]) for row in reader]))
            result.sort()
    else:
        result = []
    return result

def update_preselected_problematics(debug=False):    
    from .models import TweetRelation

    ids = get_preselected_tweet_relations_ids()
    queryset = TweetRelation.objects \
        .filter(relevant=True, id__in=ids) \
        .all()

    if debug:
        from datetime import datetime
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print('Starting <update problematics> script at :', dt_string)

    tweet_relations_to_update = []
    for tweet_relation in queryset:
        tweet_relation.problematic = True
        tweet_relations_to_update.append(tweet_relation)
    
    if debug:
        print('to update, n items = ', len(tweet_relations_to_update))

    TweetRelation.objects.bulk_update(tweet_relations_to_update,['problematic'])

    if debug:
        from datetime import datetime
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print('Finishing <update problematics> script at :', dt_string)
        print()

    return None