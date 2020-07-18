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

class Annotation(models.Model):
    tweet_relation = models.ForeignKey(TweetRelation,on_delete=models.SET_NULL,null=True)
    annotator = models.ForeignKey(Annotator,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return f'Annotation : Id={self.id}, Annotator={self.annotator.name}'
    
class Question(models.Model):
    TYPE = [("Checkbox","Checkbox"),("Choice","Choice")]
    section = models.TextField(default=None)
    value = models.TextField()
    type = models.CharField(max_length=50, choices=TYPE)
    options =  models.TextField(null=True) # json string

    def __str__(self):
        return self.value
    
    def options_list(self):
        from json import loads
        return loads(self.options)

class Answer(models.Model):   
    question = models.ForeignKey(Question,on_delete=models.SET_NULL,null=True)
    annotation = models.ForeignKey(Annotation,on_delete=models.SET_NULL,null=True)
    value = models.TextField() # json string

    def __str__(self):
        return f'Answer : Annotation={self.annotation.id}'
