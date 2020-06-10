from django.db import models

# Create your models here.

class Tweet(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.CharField(max_length=100) # TODO: Remove this field as only ID of tweet is needed to render it
    text = models.TextField(max_length=300)
    deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Tweet : Id={self.id}'

class TweetRelation(models.Model):
    TYPE=[("Quote","Quote"),("Reply","Reply")]
    tweet_source=models.ForeignKey(Tweet,on_delete=models.SET_NULL,null=True, blank=True, related_name='tweer_source')
    tweet_response=models.ForeignKey(Tweet,on_delete=models.SET_NULL,null=True, blank=True, related_name='tweer_response')
    relation_type=models.CharField(max_length=50, choices=TYPE)

class Annotator(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'Annotator : Name={self.name}, Id={self.id}'

class Stance(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=300)

    def __str__(self):
        return f'Stance : Name={self.name}'

class Confidence(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=300)

    def __str__(self):
        return f'Confidence : Name={self.name}'
    
class Expressivity(models.Model):
    type = models.CharField(max_length=30)
    value = models.BooleanField(default=False)
    evidence = models.BooleanField(default=False)

    def __str__(self):
        return f'Expressivity : Type={self.type},Value={self.value},Evidence={self.evidence}'
    
class Annotation(models.Model):
    tweet_relation = models.ForeignKey(TweetRelation,on_delete=models.SET_NULL,null=True)
    annotator = models.ForeignKey(Annotator,on_delete=models.SET_NULL,null=True)
    stance=models.ForeignKey(Stance,on_delete=models.SET_NULL,null=True)
    confidence=models.ForeignKey(Confidence,on_delete=models.SET_NULL,null=True)
    expressivity=models.ForeignKey(Expressivity,on_delete=models.SET_NULL,null=True, blank=True)

    def __str__(self):
        return f'Annotation : Annotator={self.annotator}'
    
