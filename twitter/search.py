import tweepy
from datetime import datetime, timedelta
from collections import namedtuple
import keys

Tweet = namedtuple("Tweet", "id text author_id author_name author_image author_bio")
client = tweepy.Client(keys.TWITTER_BEARER_TOKEN)


def search_tweets(last_search: datetime) -> list[Tweet]:
    with open("twitter/filters.txt", "r") as file:
        lines = file.read().split("\n")
        age = timedelta(hours=int(lines[2]))
        keywords = lines[4]
        min_retweets = int(lines[6])
        max_followers = int(lines[8])
    ret = []
    for resp in tweepy.Paginator(
            method=client.search_recent_tweets,
            start_time=last_search - age,
            end_time=datetime.utcnow() - age,
            query=f"({keywords}) -is:reply -is:retweet lang:en -is:verified",
            tweet_fields=["public_metrics"],
            expansions=["author_id"],
            user_fields=["public_metrics", "profile_image_url", "description"],
            max_results=100
    ):
        tweets = resp.data
        authors = resp.includes["users"]
        for tt in tweets:
            author = next((a for a in authors if a.id == tt.author_id))
            if tt.public_metrics["retweet_count"] >= min_retweets \
                    and author.public_metrics["followers_count"] <= max_followers:
                ret.append(Tweet(tt.id, tt.text, author.id, author.username, author.profile_image_url, author.description))
    return ret