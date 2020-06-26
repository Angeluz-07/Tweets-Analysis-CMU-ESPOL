from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quotes', views.quotes_simple_example, name='quotes'),
    path('replies', views.replies_simple_example, name='replies'),
    path('login', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
