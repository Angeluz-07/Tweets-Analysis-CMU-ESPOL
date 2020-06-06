from django.db import models

# Create your models here.

class Tweet(models.Model):
    url = models.CharField(max_length=100)
    text = models.TextField(max_length=300)
    deleted = models.BooleanField(default=False)

class TweetRelation(models.Model):
    TYPE=[("Quote","Quote"),("Reply","Reply")]
    tweet_source=models.ForeignKey(Tweet,on_delete=models.SET_NULL,null=True, blank=True, related_name='tweer_source')
    tweet_response=models.ForeignKey(Tweet,on_delete=models.SET_NULL,null=True, blank=True, related_name='tweer_response')
    relation_type=models.CharField(max_length=50, choices=TYPE)

class Annotator(models.Model):
    name = models.CharField(max_length=30)

class Stance(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=300)

    def __str__(self):
        return f'Stance : {self.name}'

class Confidence(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=300)

    def __str__(self):
        return f'Confidence : {self.name}'
    
class Expressivity(models.Model):
    type = models.CharField(max_length=30)
    value = models.BooleanField(default=False)
    evidence = models.BooleanField(default=False)

    def __str__(self):
        return f'Expressivity : Type={self.type},Value={self.value},Evidence={self.evidence}'
    
class Annotation(models.Model):
    tweet_relation = models.ForeignKey(TweetRelation,on_delete=models.SET_NULL,null=True, blank=True)
    annotator = models.ForeignKey(Annotator,on_delete=models.SET_NULL,null=True, blank=True)
    stance=models.ForeignKey(Stance,on_delete=models.SET_NULL,null=True, blank=True)
    confidence=models.ForeignKey(Confidence,on_delete=models.SET_NULL,null=True, blank=True)
    expressivity=models.ForeignKey(Expressivity,on_delete=models.SET_NULL,null=True, blank=True)
