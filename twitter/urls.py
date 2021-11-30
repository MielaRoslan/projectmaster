from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('index', views.index, name='index'),
    path('about', views.about, name="about"),
    path('apikey', views.apikey, name="apikey"),
    path('twitter_search_form', views.twitter_search_form, name="twitter_search_form"),
    path('delete_term/<term_id>', views.delete_term, name="delete_term"),
    path('run_report/<term_id>', views.run_report, name="run_report"),
    path('show_tweets/<term_id>', views.show_tweets, name="show_tweets"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('show_chart', views.show_chart, name="show_chart"),
    path('contact', views.contact, name='contact'),
    path('manage', views.manage, name='manage'),
]