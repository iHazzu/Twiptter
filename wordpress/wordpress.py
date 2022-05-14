import requests
import re
from .wp_api import WpApi
from keys import POST_TYPE, WORDPRESS_DOMAIN, WORDPRESS_USER, WORDPRESS_PASSWORD
from twitter import Tweet

wp = WpApi(
    domain=WORDPRESS_DOMAIN,
    user=WORDPRESS_USER,
    password=WORDPRESS_PASSWORD
)
URL_REGEX = re.compile(r'(https?://[^\s]+)')


def publish_tweet(tweet: Tweet):
    post = wp.get_post(POST_TYPE, f"[{tweet.author_id}]")
    if not post:
        desc = f'<i>{tweet.author_bio}</i>\n' \
               f'<a href="https://twitter.com/{tweet.author_name}" target="_blank">View Profile</a>' \
               f'<!-- Account ID: [{tweet.author_id}] -->' \
               f'<hr/>'
        desc += link_tweet_text(tweet)
        filename = f"{tweet.author_name}.jpg"
        file = requests.get(tweet.author_image.replace("_normal", "")).content
        media_id = wp.upload_image(filename, file)["id"]
        wp.create_post(POST_TYPE, tweet.author_name, desc, media_id)
    else:
        if str(tweet.id) not in post['content']['rendered']:
            desc = post['content']['rendered'] + "<hr/>" + link_tweet_text(tweet)
            wp.edit_post(POST_TYPE, post["id"], desc)


def link_tweet_text(tweet):
    text = URL_REGEX.sub(r'<a href="\1">\1</a>', tweet.text)    # making links clickable
    text += f'\n<a href="https://twitter.com/i/web/status/{tweet.id}" target="_blank">View Tweet</a>'
    return text