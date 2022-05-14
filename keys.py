from os import environ as env
from tweepy import OAuth1UserHandler


TWITTER_BEARER_TOKEN = env["TWITTER_BEARER_TOKEN"]
WORDPRESS_DOMAIN = "https://alphaleaks.com/"
WORDPRESS_USER = env["WORDPRESS_USER"]
WORDPRESS_PASSWORD = env["WORDPRESS_PASSWORD"]
POST_TYPE = "tweet"