"""
Project: Twiptter
Author: iHazzu
Function: Collects posts from Twitter and publishes to a WordPress site
Date: 07/02/2022
"""

from datetime import timedelta, datetime
from twitter import search_tweets
from wordpress import publish_tweet
import logging


# This script should run every 10 minutes
now = datetime.utcnow()
last_search = now - timedelta(minutes=10)
tweets_list = []
try:
    tweets_list = search_tweets(last_search)
    for tweet in tweets_list:   # post tweets on Wordpress
        publish_tweet(tweet)
except Exception as error:
    logging.basicConfig(filename="logs/main_logs.log", level=logging.ERROR)
    logging.exception(f" {datetime.utcnow()} - EXCEPTION: {error}\nTWEETS: {tweets_list}")