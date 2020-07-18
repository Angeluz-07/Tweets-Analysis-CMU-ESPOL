from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'questions', views.QuestionViewSet)


urlpatterns = [
    path('', RedirectView.as_view(url='annotate')),
    path('annotate', views.annotate, name='annotate'),
    path('login', auth_views.LoginView.as_view(template_name="analisis/login.html"), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('api/', include(router.urls)),
]
