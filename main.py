"""
Project: Twiptter
Author: iHazzu
Function: Collects posts from Twitter and publishes to a WordPress site
Date: 07/02/2022
"""

from datetime import timedelta, datetime
from twitter import search_tweets
from wordpress import publish_tweet
from time import sleep
import logging

logging.basicConfig(filename="logs/main_logs.log", level=logging.ERROR)
logging.debug(f'Bot running at {datetime.utcnow()}')
loop_interval = timedelta(minutes=5)
last_search = datetime.utcnow() - loop_interval
tweets_list = []
print("----| BOT RUNNING |----")


while True:
    try:
        tweets_list = search_tweets(last_search)
        last_search = datetime.utcnow()
        for tweet in tweets_list:   # post tweets on Wordpress
            publish_tweet(tweet)
    except Exception as error:
        logging.exception(f" {datetime.utcnow()} - EXCEPTION: {error}\nTWEETS: {tweets_list}")
    sleep(loop_interval.seconds)