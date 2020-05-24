from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quotes', views.quotes_simple_example, name='quotes'),
    path('replies', views.replies_simple_example, name='replies'),
]
