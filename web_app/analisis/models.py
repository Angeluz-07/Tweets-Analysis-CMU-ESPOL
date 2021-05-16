from django.db import models
from itertools import chain
from collections import Counter

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
        return f'TweetRelation {self.id} : TweetTarget={self.tweet_target}, TweetResponse={self.tweet_response}, RelationType={self.relation_type}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tweet_target', 'tweet_response'], name='unique tweet_relation for a pair of tweets')
        ]

    @property
    def is_skipped(self):
        return self.has_revision and self.revision.skipped

    @property
    def has_revision(self):
        return hasattr(self, 'revision') and self.revision is not None

    @property
    def is_resolved(self):
        return self.has_revision and self.revision.annotation_id is not None

    @property
    def annotation_inconsistent_answers(self):        
        answers = list(
            chain.from_iterable(
                [
                    a.answers.all() for a in self.annotation_set.all()
                ]
            )
        )

        answers:List[dict]  = list(map(lambda item: { 'question_id' : item.question_id , 'value' : item.value_json}, answers))

        def build_group(question_id, answers):
            _answers:List[dict] = list(filter(lambda item: item['question_id']==question_id, answers))
            _answers:List[str] = list(map(lambda item: item['value'], _answers))
            answers_relative_freq:dict[str,float] = { k : (v/len(_answers)) for k, v in dict(Counter(_answers)).items()}

            result = {
                'question_id' : question_id,
                'answers_relative_freq': answers_relative_freq,
                'total_answers' : len(_answers)
            }
            return result

        grouped:List[dict] = [ build_group(_id, answers)  for _id in self.question_ids_of_interest]

        def has_inconsistent_answers(answers_relative_freq: dict) -> bool:
            return all(list(map(lambda x: x<=0.5, answers_relative_freq.values())))
        
        def has_enough_answers(total_answers: int ) -> bool:
            return total_answers == 3

        grouped:List[dict] = [
            group for group in grouped 
            if has_inconsistent_answers(group['answers_relative_freq']) and has_enough_answers(group['total_answers'])
        ]

        return grouped

    @property
    def is_problematic(self):
        return len(self.annotation_inconsistent_answers)>0

    @property
    def annotation_inconsistent_answers_as_json(self):
        from json import dumps
        return dumps(self.annotation_inconsistent_answers)

    @property
    def question_ids_of_interest(self):
        return [2,3,4,5,6,7,9,10]

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
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tweet_relation', 'annotator'], name='unique annotation for the pair (annotator,tweet_relation)')
        ]

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
    annotation = models.ForeignKey(Annotation,on_delete=models.CASCADE, related_name='answers')
    value = models.TextField() # json string
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Answer : Annotation={self.annotation.id if self.annotation else None}'

    @property
    def value_json(self):
        from json import loads
        return loads(self.value)
    
    @property
    def tweet_relation(self):
        return self.annotation.tweet_relation.id

class Revision(models.Model):
    tweet_relation = models.OneToOneField(TweetRelation,on_delete=models.CASCADE)
    annotation = models.OneToOneField(Annotation,on_delete=models.CASCADE, null=True)
    skipped = models.BooleanField(default=False)
