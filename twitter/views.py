from django.shortcuts import render, redirect
from .models import SearchLog, APIKeys, Twitter
from django.contrib import messages
from .forms import SearchForm, APIKeysForm
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from string import punctuation
import re
from nltk.tokenize import word_tokenize
import pandas as pd
import numpy as np
from collections import Counter


analyzer = SentimentIntensityAnalyzer()

def index(request):
    return render(request, 'index.html')

# Create your views here.
def contact(request):

    return render(request, 'contact.html')

def manage(request):

    return redirect('twitter_search_form')

def twitter_search_form(request):
    terms = SearchLog.objects.all()
    print('twitter_search_form')
    for term in terms:
        term_count = Twitter.objects.filter(term=term).count()
        obj = SearchLog.objects.get(term=term)
        obj.total_tweet = term_count
        obj.save()
    terms = SearchLog.objects.all()

    if request.method == "POST":
        twitter_searchform = SearchForm(request.POST or None)
        if twitter_searchform.is_valid():
            twitter_searchform.save()
            messages.success(request, "Added to database")
            return redirect('twitter_search_form')
        else:
            messages.success(request, "Already added!!!")
            return redirect('twitter_search_form')
    else:

        if APIKeys.objects.all().exists():
            return render(request, 'manage.html', {'terms': terms})
        else:
            messages.success(request, "No API key found. Please setup the twitter api keys")
            return render(request, 'apikey.html')


def delete_term(request, term_id):
    item = SearchLog.objects.filter(pk=term_id)
    tweets = Twitter.objects.filter(term=item[0])
    item.delete()
    tweets.delete()

    messages.success(request, "Deleted Successfully!!!")
    return redirect(twitter_search_form)


def run_report(request, term_id):
    item = SearchLog.objects.filter(pk=term_id)
    print('item: ', item[0])
    if APIKeys.objects.all().exists():
        apitoken = APIKeys.objects.latest('id')
        consumer_key = apitoken.api_key
        consumer_secret = apitoken.api_secret_key
        access_token = apitoken.access_token
        access_token_secret = apitoken.access_token_secret
        # Pass OAuth details to tweepy's OAuth handler
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        # Creating the API object while passing in auth information
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        results = api.search(q=item[0], lang='en', count=100)
        print(item[0])
        objs = (Twitter(term=item[0],
                        twitterid=tweet.id,
                        created_at=tweet.created_at,
                        text=tweet.text,
                        sentimentscore=analyzer.polarity_scores(tweet.text)['compound'],
                        hastags=hashtag_extract(tweet.text),
                        screenname=tweet.user.screen_name,
                        cleaned_text=",".join(PreProcessTweets().processTweets(tweet.text, item[0])))
                for tweet in results)

        Twitter.objects.bulk_create(objs, ignore_conflicts=True)
        messages.success(request, "Successfully fetched twitter data")
        return redirect('twitter_search_form')
    else:
        return redirect('twitter_search_form')

def show_tweets(request, term_id):
    item = SearchLog.objects.filter(pk=term_id)
    tweets = Twitter.objects.filter(term=item[0])
    return render(request,'showtweets.html', {'tweets': tweets})

# Create views here.
def about(request):
    return render(request, 'about.html', {})


def apikey(request):
    if request.method == "POST":
        apiform = APIKeysForm(request.POST or None)
        if apiform.is_valid():
            apiform.save()
            messages.success(request, "API detail added to database")
            return redirect('apikey')
        else:
            messages.success(request, "Invalid data. Please try again")
            return redirect('apikey')
    else:
        return render(request, 'apikey.html')


def dashboard(request):
    terms = SearchLog.objects.all()
    return render(request, 'dashboard.html', {'terms': terms})


def show_chart(request):
    terms = SearchLog.objects.all()
    bins_cuts = [-1.0, -0.6, -0.1, 0.1, 0.6, 1.0]
    names = ['Strongly Negative', 'Negative', 'Neutral', 'Positive', 'Strongly Positive']
    if request.method == "POST":
        symbol = str(request.POST['term_value'])
        print("symbol: ", symbol)
        if symbol != "choose":
            data = Twitter.objects.filter(term=symbol)
            print('len(data)', len(data))
            ml_data = list([float(data_item.sentimentscore) for data_item in data])
            sentiment_category = pd.cut(np.array(ml_data), bins_cuts, labels=names)
            print(list(sentiment_category.value_counts()))

            # hashtags Analysis
            total_hastags = []
            for data_item in data:
                if data_item.hastags != "":
                    for tt in range(len(data_item.hastags.split(","))):
                        total_hastags.append(data_item.hastags.split(",")[tt])
            most_common = Counter(total_hastags).most_common(15)
            hastag_words = []
            hastag_count = []
            for kk in most_common:
                hastag_words.append(str(kk[0]))
                hastag_count.append(kk[1])

            # Frequent Word Analysis
            total_words = []
            for data_item in data:
                if data_item.cleaned_text != "":
                    for pp in range(len(data_item.cleaned_text.split(","))):
                        total_words.append(data_item.cleaned_text.split(",")[pp])
            most_common = Counter(total_words).most_common(15)
            cleaned_words = []
            cleaned_count = []
            for qq in most_common:
                cleaned_words.append(str(qq[0]))
                cleaned_count.append(qq[1])


            # Frequent Positive Word Analysis
            pos_total_words = []
            for data_item in data:
                if data_item.cleaned_text != "" and data_item.sentimentscore >= 0.6:
                    for pos_pp in range(len(data_item.cleaned_text.split(","))):
                        pos_total_words.append(data_item.cleaned_text.split(",")[pos_pp])

            most_common = Counter(pos_total_words).most_common(15)
            pos_cleaned_words = []
            pos_cleaned_count = []
            print(most_common)
            for pos_qq in most_common:
                pos_cleaned_words.append(str(pos_qq[0]))
                pos_cleaned_count.append(pos_qq[1])

            # Frequent Negative Word Analysis
            neg_total_words = []
            for data_item in data:
                if data_item.cleaned_text != "" and data_item.sentimentscore <= -0.6:
                    for neg_pp in range(len(data_item.cleaned_text.split(","))):
                        neg_total_words.append(data_item.cleaned_text.split(",")[neg_pp])
            most_common = Counter(neg_total_words).most_common(15)
            neg_cleaned_words = []
            neg_cleaned_count = []
            for neg_qq in most_common:
                neg_cleaned_words.append(str(neg_qq[0]))
                neg_cleaned_count.append(neg_qq[1])

            return render(request, 'dashboard.html', {'sentimentcat': list(sentiment_category.value_counts()),
                                                      'hastag_words': hastag_words,
                                                      'hastag_count': hastag_count,
                                                      'cleaned_words': cleaned_words,
                                                      'cleaned_count': cleaned_count,
                                                      'pos_cleaned_words': pos_cleaned_words,
                                                      'pos_cleaned_count': pos_cleaned_count,
                                                      'neg_cleaned_words': neg_cleaned_words,
                                                      'neg_cleaned_count': neg_cleaned_count,
                                                      'terms': terms
                                                      })
        else:
            messages.success(request, "Please select the Term")
            return redirect('dashboard')
    else:
        return redirect('dashboard')


# function to collect hashtags
def hashtag_extract(x):
    hashtags = []
    # Loop over the words in the tweet
    for i in x.split(" "):
        ht = re.findall(r"#(\w+)", i)
        if len(ht) > 0:
            hashtags.append(ht[0].lower())

    return ",".join(hashtags)


class PreProcessTweets:
    def __init__(self):
        self._stopwords = set(stopwords.words('english') + list(punctuation) + ['AT_USER', 'URL', 'RT', "n't", "..."])

    def processTweets(self, tweet, term):
        tweet = tweet.lower()  # convert text to lower-case
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', ' ', tweet)  # remove URLs
        tweet = re.sub('@[^\s]+', ' ', tweet)  # remove usernames
        tweet = re.sub('[^a-zA-Z#]', ' ', tweet)
        tweet = word_tokenize(tweet)  # remove repeated characters (helloooooooo into hello)

        return [word for word in tweet if (word not in self._stopwords) & (len(word) > 3) & (word != term)]

