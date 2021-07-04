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