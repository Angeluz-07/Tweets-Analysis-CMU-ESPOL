from django.test import TestCase
from analisis.models import Tweet, TweetRelation, Annotator, Annotation
from analisis.views import get_random_tweet_relation
from unittest.mock import patch, Mock

# Create your tests here.
class AnnotatorAnnotatesTweetOnce(TestCase):

    def setUp(self):
        """
        Create Annotator
        Create four Tweets
        """
        self.annotator = Annotator.objects.create(id=100)
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
        Annotation.objects.create(
            annotator_id = self.annotator.id,
            tweet_relation_id = self.tweet_relation_annotated.id
        )

    @patch('analisis.views.get_random_tweet_relation_type',Mock(return_value=('Quote','')))
    def test_tweet_relation_already_annotated_by_user_is_not_retrieved(self):
        tr = get_random_tweet_relation(self.annotator.id, False)
        self.assertEqual(tr.id, self.tweet_relation_non_annotated.id)


class TweetAnnotatedThriceIsNotRetrieved(TestCase):

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
        self.tweet_relation_annotated_thrice = TweetRelation.objects.create(
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
        Create three Annotators
        Annotate one TweetRelation three times
        """
        for ann_id in [100, 200, 300]:
            Annotator.objects.create(id=ann_id)
            Annotation.objects.create(
                annotator_id=ann_id,
                tweet_relation_id=self.tweet_relation_annotated_thrice.id
            )

    @patch('analisis.views.get_random_tweet_relation_type',Mock(return_value=('Quote','')))
    def test_tweet_relation_annotated_thrice_is_not_retrieved(self):
        tr = get_random_tweet_relation(100, False)
        self.assertEqual(tr.id, self.tweet_relation_non_annotated.id)


class TweetNonAnnotatedIsNotRetrievedInEagerMode(TestCase):

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
        self.tweet_relation_annotated_once = TweetRelation.objects.create(
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
        Annotate one TweetRelation
        """
        annotator_id = 100
        Annotator.objects.create(id=annotator_id)
        Annotation.objects.create(
            annotator_id=annotator_id,
            tweet_relation_id=self.tweet_relation_annotated_once.id
        )

    @patch('analisis.views.get_random_tweet_relation_type',Mock(return_value=('Quote','')))
    def test_tweet_relation_non_annotated_is_not_retrieved_in_eager_mode(self):
        another_annotator_id = 101
        tr = get_random_tweet_relation(another_annotator_id)
        self.assertEqual(tr.id, self.tweet_relation_annotated_once.id)
