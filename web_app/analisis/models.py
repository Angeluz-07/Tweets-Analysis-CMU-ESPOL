from django.db import models

# Create your models here.

class Tweet(models.Model):
    id = models.BigIntegerField(primary_key=True)
    text = models.TextField(max_length=300)
    deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Tweet : Id={self.id}'

class TweetRelation(models.Model):
    TYPE=[("Quote","Quote"),("Reply","Reply")]
    tweet_target=models.ForeignKey(Tweet,on_delete=models.SET_NULL,null=True, blank=True, related_name='tweet_target')
    tweet_response=models.ForeignKey(Tweet,on_delete=models.SET_NULL,null=True, blank=True, related_name='tweet_response')
    relation_type=models.CharField(max_length=50, choices=TYPE)

    def __str__(self):
        return f'TweetRelation : TweetTarget={self.tweet_target}, TweetResponse={self.tweet_response}, RelationType={self.relation_type}'

class Annotator(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

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
    
