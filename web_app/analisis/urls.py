from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='annotate/Quote')),
    path('annotate/<str:relation_type>', views.annotate, name='annotate'),
    path('login', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
