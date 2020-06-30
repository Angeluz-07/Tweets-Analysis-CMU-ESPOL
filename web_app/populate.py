# source: https://www.tangowithdjango.com/book17/chapters/models.html
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'analisistweets.settings')

import django
django.setup()

from analisis.models import Stance, Confidence, Expressivity, Tweet, TweetRelation, Annotator
from django.contrib.auth.models import User
import csv
import json

def random_password(length=10):
    from string import digits, ascii_letters
    from random import choices, shuffle
    chars = list(f"{digits}{ascii_letters}!#$%&'*+-<=>?@^_|~")
    shuffle(chars)
    result = choices(chars, k=length)
    return ''.join(result)

def add_annotators():
    with open('data/Lista_anotadores.csv') as csv_file:            
        rows = list(csv.reader(csv_file, delimiter=','))
        for row in rows:
            username = row[1] #same as email
            password = row[2]
            u, _ = User.objects.get_or_create(username=username)
            u.set_password(password)
            u.save()
            print(u)

            #Mirror an annotator with same id as user
            name = row[0]
            name = name.strip('"').replace(',',' ')
            a, _ = Annotator.objects.get_or_create(id=u.id, name=name)
            print(a)


def add_tweet_and_tweet_relations():
    # TODO: Update this code with the final format of data to feed DB.
    # Load tweet_texts in memory
    data = []
    with open('data/tweet_database.json') as f:
        for line in f:
            data.append(json.loads(line))

    tweet_text_by_tweet_id = { item['tweet_id'] : item['tweet_text'] for item in data }
    # Add tweets
    with open('data/pair_database.csv') as csv_file:            
        rows = list(csv.reader(csv_file, delimiter=','))

        #for row in rows[1:500]: #<-- a little limit for test and debugging
        for row in rows[1:]:
            response_id : str = row[1]
            target_id : str = row[2]

            if response_id in tweet_text_by_tweet_id \
               and target_id in tweet_text_by_tweet_id:
                t, _ = Tweet.objects.get_or_create(
                    id = int(response_id),
                    text = tweet_text_by_tweet_id[response_id]
                )
                print(t)

                t, _ = Tweet.objects.get_or_create(
                    id = int(target_id),
                    text = tweet_text_by_tweet_id[target_id]
                )
                print(t)

                interaction_type = row[3]
                tr, _ = TweetRelation.objects.get_or_create(
                    tweet_target_id = int(target_id),
                    tweet_response_id = int(response_id),
                    relation_type = interaction_type
                )
                print(tr)

def add_stances():
    stances = [
        {
            "name" : "Explicit Support", 
            "description" : "Cuando el tweet de respuesta expresa de forma explícita (incluye lenguaje) que esta de acuerdo con lo expresado en el tweet orginal o que este es cierto."
        },
        {
            "name" : "Implicit Support", 
            "description" : "Cuando el tweet de respuesta implica (da a entender) que esta de acuerdo con lo expresado en el tweet orginal o que este es cierto."
        },
        {
            "name" : "Comment",
            "description" : "Cuando el tweet the respuesta es neutral al, o solo comenta el, contenido del tweet original."
        },
        {
            "name" : "Queries", # Pregunta por más información
            "description" : "Cuando el tweet de respuesta pregunta por mas información sobre contenido del tweet original."
        },
        {
            "name" : "Implicit Denial",
            "description" : "Cuando el tweet de respuesta implica (da a entender) que esta en desacuerdo con lo expresado en el tweet orginal o que este es falso."
        },
        { 
            "name" : "Explicit Denial",
            "description" : "Cuando el tweet de respuesta expresa de forma explícita (incluye lenguaje) que esta en desacuerdo con lo expresado en el tweet orginal o que este es falso."
        }
    ]
    for stance in stances:          
        s, _ = Stance.objects.get_or_create(
            name=stance['name'],
            description=stance['description']
        )
        print(s)

def add_confidences():
    confidences = [
        {
            "name" : "Sure"
        },
        {
            "name" : "Not Sure"
        },
        {
            "name" : "Some Sure"
        }
    ]
    for confidence in confidences:
        c, _=Confidence.objects.get_or_create(name=confidence['name'])
        print(c)

def add_expressivities():
    expressivities = [
        { "type" : "Fake News", "value" : True, "evidence" : True },
        { "type" : "Fake News", "value" : True, "evidence" : False },
        { "type" : "Fake News", "value" : False, "evidence" : True },
        { "type" : "Fake News", "value" : False, "evidence" : False },
        { "type" : "True News", "value" : True, "evidence" : True },
        { "type" : "True News", "value" : True, "evidence" : False },
        { "type" : "True News", "value" : False, "evidence" : True },
        { "type" : "True News", "value" : False, "evidence" : False },
    ]
    for expressivity in expressivities:
        e, _=Expressivity.objects.get_or_create(
            type=expressivity['type'],
            value=expressivity['value'],
            evidence=expressivity['evidence']
        )
        print(e)

if __name__ == '__main__':
    print("Starting population script...")
    add_stances()
    add_confidences()
    add_expressivities()
    add_tweet_and_tweet_relations()
    add_annotators()
