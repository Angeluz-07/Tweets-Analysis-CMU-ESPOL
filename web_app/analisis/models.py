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
    relevant = models.BooleanField(default=True)

    def __str__(self):
        return f'TweetRelation : TweetTarget={self.tweet_target}, TweetResponse={self.tweet_response}, RelationType={self.relation_type}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tweet_target', 'tweet_response'], name='unique tweet_relation for a pair of tweets')
        ]

class Annotator(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'Annotator : Name={self.name}, Id={self.id}'

class Annotation(models.Model):
    tweet_relation = models.ForeignKey(TweetRelation,on_delete=models.SET_NULL,null=True)
    annotator = models.ForeignKey(Annotator,on_delete=models.SET_NULL,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    time_spent = models.IntegerField(null=True)

    def __str__(self):
        return f'Annotation : Id={self.id}, Annotator={self.annotator.name if self.annotator else None}'
    
    # First remove duplicates in DB, then apply migration
    #class Meta:
    #    constraints = [
    #        models.UniqueConstraint(fields=['tweet_relation', 'annotator'], name='unique annotation for the pair (annotator,tweet_relation)')
    #    ]

class Question(models.Model):
    TYPE = [("Checkbox","Checkbox"),("Choice","Choice")]
    name = models.TextField()
    section = models.TextField()
    value = models.TextField()
    type = models.CharField(max_length=50, choices=TYPE)
    options =  models.TextField() # json string

    def __str__(self):
        return self.value
    
    def options_list(self):
        from json import loads
        return loads(self.options)

class Answer(models.Model):   
    question = models.ForeignKey(Question,on_delete=models.SET_NULL,null=True)
    annotation = models.ForeignKey(Annotation,on_delete=models.SET_NULL,null=True)
    value = models.TextField() # json string
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Answer : Annotation={self.annotation.id if self.annotation else None}'
