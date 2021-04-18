# source: https://www.tangowithdjango.com/book17/chapters/models.html
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'analisistweets.settings')

import django
django.setup()

from analisis.models import *
import json

def add_tweet_and_tweet_relations():
    # Load tweet_texts in memory
    data = []
    with open('data/second_run_database.json') as f:
        for line in f:
            data.append(json.loads(line))

    for info in data[:10]: #<-- a little limit for test and debugging
    #for info in data:
        tweet_target_id = int(info['tweet_target_id'])
        tweet_target_text = info['tweet_target_text'].encode('unicode_escape') #this encode is neccesary because we use MYSQL. Postgresql doesnt need it.

        tweet_response_id = int(info['tweet_response_id'])
        tweet_response_text = info['tweet_response_text'].encode('unicode_escape')

        interaction_type = info['interaction_type']

        
        try:                     
            t, _ = Tweet.objects.get_or_create(
                id = tweet_target_id,
                text = tweet_target_text
            )
        except Exception as e:
            from django.db.utils import IntegrityError
            if isinstance(e, IntegrityError):
                t = Tweet.objects.get(
                    id = tweet_target_id
                )
                t.text = tweet_target_text
                t.save()
        finally:       
            print(t)

        try:
            t, _ = Tweet.objects.get_or_create(
                id = tweet_response_id,
                text = tweet_response_text
            )
        except Exception as e:
            from django.db.utils import IntegrityError
            if isinstance(e, IntegrityError):      
                t = Tweet.objects.get(
                    id = tweet_response_id
                )                
                t.text = tweet_response_text
                t.save()
        finally:
            print(t)
        

        try:
            tr, _ = TweetRelation.objects.get_or_create(
                tweet_target_id = tweet_target_id,
                tweet_response_id = tweet_response_id,
                relation_type = interaction_type,
                relevant=True
            )
        except Exception as e:
            from django.db.utils import IntegrityError
            if isinstance(e, IntegrityError):
                # "Existing as non-relevant, setting relevant to true"
                tr = TweetRelation.objects.get(
                    tweet_target_id = tweet_target_id,
                    tweet_response_id = tweet_response_id,
                    relation_type = interaction_type,
                )
                tr.relevant = True
                tr.save()
                print('existing',end=' - ')
        finally:
            print(tr)


if __name__ == '__main__':
    print("Starting population relevant script...")    
    add_tweet_and_tweet_relations()
