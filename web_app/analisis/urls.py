from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'questions', views.QuestionViewSet)
router.register(r'answers', views.AnswerViewSet)
router.register(r'custom-config',views.AppCustomConfigViewSet)
router.register(r'revisions',views.RevisionViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('annotate', views.annotate, name='annotate'),
    path('problematic-tweet-relations', views.problematic_tweet_relations, name='problematic_tweet_relations'),
    path('all-annotations-count', views.all_annotations_count, name='all_annotations_count'),
    path('resolve-tweet-relation/<int:tweet_relation_id>', views.resolve_tweet_relation, name="resolve_tweet_relation"),
    path('login', auth_views.LoginView.as_view(template_name="analisis/login.html"), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('api/', include(router.urls)),
    path('api/tweet-relation/random/<int:annotator_id>', views.GET_random_tweet_relation, name="GET_random_tweet_relation")
]
