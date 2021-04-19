from django.test import TestCase, TransactionTestCase
from analisis.models import Tweet, TweetRelation, Annotator, Annotation
from analisis.views import get_random_tweet_relation, create_annotation
from unittest.mock import patch, Mock

# Create your tests here.
class TweetAnnotatedByUser(TestCase):

    def setUp(self):
        """
        Create four Tweets
        """
        for tt_id, tr_id in [(100,101),(200,201)]:
            Tweet.objects.create(id=tt_id)
            Tweet.objects.create(id=tr_id)

        """
        Create two TweetRelations
        """
        self.tweet_relation_annotated = TweetRelation.objects.create(
            tweet_target_id = 100,
            tweet_response_id = 101,
            relation_type = 'Quote'
        )
        self.tweet_relation_non_annotated = TweetRelation.objects.create(
            tweet_target_id = 200,
            tweet_response_id = 201,
            relation_type = 'Quote'
        )

        """
        Create Annotation for one TweetRelation and left the other non-annotated
        """
        self.annotator = Annotator.objects.create(id=100)
        Annotation.objects.create(
            annotator_id = self.annotator.id,
            tweet_relation_id = self.tweet_relation_annotated.id
        )

    def test_is_not_retrieved(self):
        tr = get_random_tweet_relation(self.annotator.id)
        self.assertEqual(tr.id, self.tweet_relation_non_annotated.id)


class TweetAnnotatedTwice(TestCase):

    def setUp(self):
        """
        Create six Tweets
        """

        for tt_id, tr_id in [(100,101),(200,201),(300,301)]:
            Tweet.objects.create(id=tt_id)
            Tweet.objects.create(id=tr_id)

        """
        Create three TweetRelations
        """
        self.tweet_relation_annotated_once = TweetRelation.objects.create(
            tweet_target_id = 100,
            tweet_response_id = 101,
            relation_type = 'Quote'
        )

        self.tweet_relation_annotated_twice = TweetRelation.objects.create(
            tweet_target_id = 200,
            tweet_response_id = 201,
            relation_type = 'Quote'
        )

        self.tweet_relation_annotated_thrice = TweetRelation.objects.create(
            tweet_target_id = 300,
            tweet_response_id = 301,
            relation_type = 'Quote'
        )

        """
        Create one Annotator
        Annotate one TweetRelation once
        """
        annotator_id = 100
        Annotator.objects.create(id=annotator_id)
        Annotation.objects.create(
            annotator_id=annotator_id,
            tweet_relation_id=self.tweet_relation_annotated_once.id
        )

        """
        Create two Annotators
        Annotate one TweetRelation twice
        """
        for ann_id in [200, 300]:
            Annotator.objects.create(id=ann_id)
            Annotation.objects.create(
                annotator_id=ann_id,
                tweet_relation_id=self.tweet_relation_annotated_twice.id
            )

        """
        Create three Annotators
        Annotate one TweetRelation three times
        """
        for ann_id in [400, 500, 600]:
            Annotator.objects.create(id=ann_id)
            Annotation.objects.create(
                annotator_id=ann_id,
                tweet_relation_id=self.tweet_relation_annotated_thrice.id
            )

    def test_is_retrieved(self):
        annotator_id = 700
        Annotator.objects.create(id=annotator_id)
        tr = get_random_tweet_relation(annotator_id)
        self.assertEqual(tr.id, self.tweet_relation_annotated_twice.id)

class TweetAnnotatedOnce(TestCase):

    def setUp(self):
        """
        Create six Tweets
        """

        for tt_id, tr_id in [(100,101),(200,201),(300,301)]:
            Tweet.objects.create(id=tt_id)
            Tweet.objects.create(id=tr_id)

        """
        Create three TweetRelations
        """
        self.tweet_relation_annotated_zero = TweetRelation.objects.create(
            tweet_target_id = 100,
            tweet_response_id = 101,
            relation_type = 'Quote'
        )

        self.tweet_relation_annotated_once = TweetRelation.objects.create(
            tweet_target_id = 200,
            tweet_response_id = 201,
            relation_type = 'Quote'
        )

        self.tweet_relation_annotated_thrice = TweetRelation.objects.create(
            tweet_target_id = 300,
            tweet_response_id = 301,
            relation_type = 'Quote'
        )

        """
        Create one Annotator
        Annotate one TweetRelation once
        """
        annotator_id = 100
        Annotator.objects.create(id=annotator_id)
        Annotation.objects.create(
            annotator_id=annotator_id,
            tweet_relation_id=self.tweet_relation_annotated_once.id
        )

        """
        Create three Annotators
        Annotate one TweetRelation three times
        """
        for ann_id in [200, 300, 400]:
            Annotator.objects.create(id=ann_id)
            Annotation.objects.create(
                annotator_id=ann_id,
                tweet_relation_id=self.tweet_relation_annotated_thrice.id
            )

    def test_is_retrieved(self):
        annotator_id = 500
        Annotator.objects.create(id=annotator_id)
        tr = get_random_tweet_relation(annotator_id)
        self.assertEqual(tr.id, self.tweet_relation_annotated_once.id)

class TweetAnnotatedZero(TestCase):

    def setUp(self):
        """
        Create four Tweets
        """

        for tt_id, tr_id in [(100,101),(200,201)]:
            Tweet.objects.create(id=tt_id)
            Tweet.objects.create(id=tr_id)

        """
        Create two TweetRelations
        """
        self.tweet_relation_annotated_zero = TweetRelation.objects.create(
            tweet_target_id = 100,
            tweet_response_id = 101,
            relation_type = 'Quote'
        )

        self.tweet_relation_annotated_thrice = TweetRelation.objects.create(
            tweet_target_id = 200,
            tweet_response_id = 201,
            relation_type = 'Quote'
        )


        """
        Create three Annotators
        Annotate one TweetRelation three times
        """
        for ann_id in [100, 200, 300]:
            Annotator.objects.create(id=ann_id)
            Annotation.objects.create(
                annotator_id=ann_id,
                tweet_relation_id=self.tweet_relation_annotated_thrice.id
            )

    def test_is_retrieved(self):
        annotator_id = 400
        Annotator.objects.create(id=annotator_id)
        tr = get_random_tweet_relation(annotator_id)
        self.assertEqual(tr.id, self.tweet_relation_annotated_zero.id)

class AllTweetsAnnotated(TestCase):

    def setUp(self):
        """
        Create two Tweets
        """

        for tt_id, tr_id in [(100,101)]:
            Tweet.objects.create(id=tt_id)
            Tweet.objects.create(id=tr_id)

        """
        Create one TweetRelation
        """
        self.tweet_relation_annotated_thrice = TweetRelation.objects.create(
            tweet_target_id = 100,
            tweet_response_id = 101,
            relation_type = 'Quote'
        )


        """
        Create three Annotators
        Annotate one TweetRelation three times
        """
        for ann_id in [100, 200, 300]:
            Annotator.objects.create(id=ann_id)
            Annotation.objects.create(
                annotator_id=ann_id,
                tweet_relation_id=self.tweet_relation_annotated_thrice.id
            )

    def test_none_is_retrieved(self):
        annotator_id = 400
        Annotator.objects.create(id=annotator_id)
        tr = get_random_tweet_relation(annotator_id)
        self.assertEqual(tr, None)

class TweetAnnotationRelevant(TestCase):

    def setUp(self):
        """
        Create two Tweets
        """
        for tt_id, tr_id in [(100,101)]:
            Tweet.objects.create(id=tt_id)
            Tweet.objects.create(id=tr_id)

        """
        Create a TweetRelation
        """
        TweetRelation.objects.create(
            tweet_target_id = 100,
            tweet_response_id = 101,
            relation_type = 'Quote',
            relevant=False
        )

    def test_is_not_retrieved(self):
        tr = get_random_tweet_relation(annotator_id=100)
        self.assertEqual(tr, None)

class TweetRelationUnique(TransactionTestCase):

    def setUp(self):
        """
        Create two Tweets
        """
        for tt_id, tr_id in [(100,101)]:
            Tweet.objects.create(id=tt_id)
            Tweet.objects.create(id=tr_id)

        """
        Create one TweetRelation
        """
        self.tweet_relation_valid = TweetRelation.objects.create(
            tweet_target_id = 100,
            tweet_response_id = 101,
            relation_type = 'Quote'
        )

    def test_error_on_duplicate(self):
        try:
            tweet_relation_invalid = TweetRelation.objects.create(
                tweet_target_id = 100,
                tweet_response_id = 101,
                relation_type = 'Quote'
            )
        except Exception as e:
            from django.db.utils import IntegrityError
            self.assertIsInstance(e, IntegrityError)
        finally:
            self.assertEqual(TweetRelation.objects.all().count(), 1)

class AnnotationOnTweetUniqueByAnnotator(TransactionTestCase):

    def setUp(self):
        """
        Create two Tweets
        """
        for tt_id, tr_id in [(100,101)]:
            Tweet.objects.create(id=tt_id)
            Tweet.objects.create(id=tr_id)

        """
        Create one TweetRelation
        """
        self.tweet_relation_annotated = TweetRelation.objects.create(
            tweet_target_id = 100,
            tweet_response_id = 101,
            relation_type = 'Quote'
        )

        """
        Create one annotator
        """
        self.annotator = Annotator.objects.create(id='100')

        """
        Create one annotation for given tweet_relation
        """
        self.first_annotation = Annotation.objects.create(
            annotator_id = self.annotator.id,
            tweet_relation_id = self.tweet_relation_annotated.id
        )


    def test_error_on_duplicate(self):
        form_data = {
            'annotator_id' : self.annotator.id,
            'tweet_relation_id' : self.tweet_relation_annotated.id,
            'time_spent' : 10
        }
        create_annotation(form_data)
        self.assertEqual(Annotation.objects.all().count(), 1)
