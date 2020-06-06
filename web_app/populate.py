# source: https://www.tangowithdjango.com/book17/chapters/models.html
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'analisistweets.settings')

import django
django.setup()

from analisis.models import Stance, Confidence, Expressivity

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
        { "type" : "fake_news", "value" : True, "evidence" : True },        
        { "type" : "fake_news", "value" : True, "evidence" : False },        
        { "type" : "fake_news", "value" : False, "evidence" : True },        
        { "type" : "fake_news", "value" : False, "evidence" : False },        
        { "type" : "true_news", "value" : True, "evidence" : True },        
        { "type" : "true_news", "value" : True, "evidence" : False },        
        { "type" : "true_news", "value" : False, "evidence" : True },        
        { "type" : "true_news", "value" : False, "evidence" : False },
    ]
    for expressivity in expressivities:
        e, _=Expressivity.objects.get_or_create(
            type=expressivity['type'],
            value=expressivity['value'],
            evidence=expressivity['evidence']
        )
        print(e)

def populate():
    add_stances()
    add_confidences()
    add_expressivities()

if __name__ == '__main__':
    print("Starting population script...")
    populate()