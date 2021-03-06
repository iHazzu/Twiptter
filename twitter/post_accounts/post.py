from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import requests
import tweepy
from os import environ as env
import re
import logging
from datetime import datetime


mentions = ""
try:
    WP_URL = f"https://alphaleaks.com/wp-json/wp/v2/tweet"
    FONT = ImageFont.truetype("Roboto.ttf", 40)

    # Connect to Twitter
    TWITTER_AUTH = tweepy.OAuth1UserHandler(
        env["API_KEY"],
        env["API_KEY_SECRET"],
        env["ACCESS_TOKEN"],
        env["ACCESS_TOKEN_SECRET"]
    )
    api = tweepy.API(TWITTER_AUTH)

    # Model image
    img = Image.open("model_accounts_post.png").convert("RGB")

    # Get accounts
    dw = ImageDraw.Draw(img, "RGBA")
    y = 200
    params = {
        'per_page': 5,
        'orderby': "modified",
        'order': "desc"
    }
    posts = requests.get(WP_URL, params=params).json()

    # Write accounts
    for p in posts:
        match = re.search(r'Account ID: \[\d+', p['content']['rendered'])
        account_id = match.group()[13:]
        user = api.get_user(user_id=account_id)
        profile_img = requests.get(user.profile_image_url).content
        with Image.open(BytesIO(profile_img)).resize((90, 90)) as acc_img:
            img.paste(im=acc_img, box=(243, y))
        dw.text(xy=(415, y+20), text=user.name, font=FONT, fill=(255, 255, 255))
        mentions += f'• @{user.screen_name}\n'
        y += 127

    # Save image as object file
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    # Tweet message
    with open('post_message.txt', 'r', encoding='utf8') as file:
        text = file.read().format(mentions)

    # Post on Twitter
    api.update_status_with_media(status=text, filename="whitelist.png", file=img_bytes)

except Exception as error:
    logging.basicConfig(filename="logs/post_logs.log", level=logging.ERROR)
    logging.exception(f" {datetime.utcnow()} - EXCEPTION: {error}\nACCOUNTS: {mentions}")


