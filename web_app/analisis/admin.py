from django.contrib import admin

from .models import *
models = [
    Tweet,
    TweetRelation,
    Annotator,
    #Stance,
    #Confidence,
    #Expressivity,
    Question,
    Answer,
    Annotation,
]
for model in models:
    admin.site.register(model)

# Register your models here.
