from django.test import TestCase, TransactionTestCase
from analisis.models import Tweet, TweetRelation, Annotator, Annotation, Question, Answer, Revision
from analisis.views import get_random_tweet_relation, create_annotation, get_problematic_tweet_relations
from unittest.mock import patch, MagicMock

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

    @patch('analisis.views.get_ids_in_cache',MagicMock(return_value=[]))
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

    @patch('analisis.views.get_ids_in_cache',MagicMock(return_value=[]))
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

    @patch('analisis.views.get_ids_in_cache',MagicMock(return_value=[]))
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

    @patch('analisis.views.get_ids_in_cache',MagicMock(return_value=[]))
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

    @patch('analisis.views.get_ids_in_cache',MagicMock(return_value=[]))
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

    @patch('analisis.views.get_ids_in_cache',MagicMock(return_value=[]))
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


class ProblematicTweetRelation(TransactionTestCase):

    def setUp(self):
        self.tweet_relation_problematic = TweetRelation.objects.create(
            id=1,
            tweet_target_id = None,
            tweet_response_id = None,
            relation_type = 'Quote'
        )
   
        self.tweet_relation_non_problematic = TweetRelation.objects.create(
            id=2,
            tweet_target_id = None,
            tweet_response_id = None,
            relation_type = 'Quote'
        )

        def _setup_annotations_question_and_answers(tweet_relation_id, question_id, annotation_ids, answer_values):
            assert len(annotation_ids) == len(answer_values)
            for i in annotation_ids:
                Annotation.objects.get_or_create(
                    id=i,
                    annotator_id = None,
                    tweet_relation_id = tweet_relation_id
                )

            Question.objects.create(id=question_id)

            for answer_value, annotation_id in zip(answer_values, annotation_ids):
                Answer.objects.create(
                    value=answer_value,
                    question_id=question_id,
                    annotation_id=annotation_id
                )

        # use ids different from  as we exclude their corresponding question in prod [1,9,10,11]
        _setup_annotations_question_and_answers(
            self.tweet_relation_problematic.id,
            question_id=3, 
            annotation_ids=[1,2,3], 
            answer_values=[ "\"Si\"", "\"No\"", "\"No es claro\""]
        )

        # consistent answers for a teetrelation that is problematic because of answers in another question
        _setup_annotations_question_and_answers(
            self.tweet_relation_problematic.id,
            question_id=4, 
            annotation_ids=[1,2,3], 
            answer_values=[ "\"Si\"", "\"No\"", "\"No\""]
        )

        _setup_annotations_question_and_answers(
            self.tweet_relation_non_problematic.id,
            question_id=5, 
            annotation_ids=[4,5,6], 
            answer_values=[ "\"Si\"", "\"No\"", "\"No\""]
        )

        from django.contrib.auth.models import User
        self.user = User.objects.create(
            username='testuser', 
            email='test@example.com', 
            password='testpass', 
            is_superuser=True
        )

    def test_problematic_tweets_are_updated(self):
        from analisis.domain import update_problematics
        update_problematics()
        
        tr_problematic_from_db = TweetRelation.objects.get(id=self.tweet_relation_problematic.id)
        self.assertTrue(tr_problematic_from_db.problematic)

        tr_non_problematic_from_db = TweetRelation.objects.get(id=self.tweet_relation_non_problematic.id)
        self.assertFalse(tr_non_problematic_from_db.problematic)

    def test_problematic_tweets_are_identified(self):
        from django.db.models import Count
        trs = TweetRelation.objects \
        .filter(relevant=True) \
        .annotate(annotation_count=Count('annotation')) \
        .filter(annotation_count__exact=3) \
        .prefetch_related('annotation_set__answers')

        from analisis.domain import tweet_relation_is_problematic
        problematic_tweet_relations = [
            tr for tr in trs if tweet_relation_is_problematic(tr)
        ]
  
        self.assertIn(self.tweet_relation_problematic, problematic_tweet_relations)
        self.assertNotIn(self.tweet_relation_non_problematic, problematic_tweet_relations)

    def test_redirect_tweet_not_problematic(self):  
        self.client.force_login(self.user)
        response = self.client.get(f'/resolve-tweet-relation/{self.tweet_relation_non_problematic.id}')
        self.assertRedirects(response, '/problematic-tweet-relations')

    def test_first_time_skipped_create_revision_without_annotation(self):
        self.client.force_login(self.user)

        self.tweet_relation_problematic.problematic = True
        self.tweet_relation_problematic.save()

        response = self.client.post(
            f'/resolve-tweet-relation/{self.tweet_relation_problematic.id}',
            data={ 'skipped': True }
        )

        revision_created = Revision.objects.get(tweet_relation_id=self.tweet_relation_problematic.id)

        assert revision_created.annotation is None
        assert revision_created.skipped is True


    @patch('analisis.views.create_annotation')
    def test_already_skipped_update_revision_on_annotation(self, create_annotation_mock):
        # context
        self.client.force_login(self.user)

        self.tweet_relation_problematic.problematic = True
        self.tweet_relation_problematic.save()

        revision = Revision.objects.create(
            tweet_relation_id=self.tweet_relation_problematic.id,
            annotation=None
        )
    
        create_annotation_mock.return_value = Annotation.objects.create(
            tweet_relation_id=self.tweet_relation_problematic.id
        )

        # test
        response = self.client.post(
            f'/resolve-tweet-relation/{self.tweet_relation_problematic.id}',
            data={}
        )

        revision_updated = Revision.objects.get(
            tweet_relation_id = self.tweet_relation_problematic.id
        )

        self.assertIsNotNone(revision_updated.annotation)


    @patch('analisis.views.create_annotation')
    def test_resolve_tweetrelation_on_first_revision(self, create_annotation_mock):
        # context
        self.client.force_login(self.user)

        self.tweet_relation_problematic.problematic = True
        self.tweet_relation_problematic.save()

        revision = Revision.objects.create(
            tweet_relation_id=self.tweet_relation_problematic.id,
            annotation=None
        )
    
        create_annotation_mock.return_value = Annotation.objects.create(
            tweet_relation_id=self.tweet_relation_problematic.id
        )

        # test
        response = self.client.post(
            f'/resolve-tweet-relation/{self.tweet_relation_problematic.id}',
            data={}
        )

        revision = Revision.objects.filter(
            tweet_relation_id = self.tweet_relation_problematic.id
        ).first()
        annotation = Annotation.objects.filter(
            tweet_relation_id = self.tweet_relation_problematic.id,
            revision__id = revision.id
        ).first()

        self.assertIsNotNone(revision)
        self.assertIsNotNone(annotation)
        self.assertEqual(revision.annotation.id, annotation.id)
        self.assertEqual(revision.skipped, False)

    
    #@patch('analisis.views.create_annotation')
    #def test_problematic_is_not_retrieved_after_resolve(self, create_annotation_mock):
    #    # context
    #    self.client.force_login(self.user)

    #    self.tweet_relation_problematic.problematic = True
    #    self.tweet_relation_problematic.save()

    #    create_annotation_mock.return_value = Annotation.objects.create(
    #        tweet_relation_id=self.tweet_relation_problematic.id
    #    )
        
    #    response = self.client.post(
    #        f'/resolve-tweet-relation/{self.tweet_relation_problematic.id}',
    #        data={}
    #    )

    #    #test

    #    problematic_tweet_relations = get_problematic_tweet_relations()

    #    self.assertNotIn(self.tweet_relation_problematic, problematic_tweet_relations)

