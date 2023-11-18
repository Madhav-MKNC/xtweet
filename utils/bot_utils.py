# -*- coding: utf-8 -*-
# author: Madhav Kumar (https://github.com/madhav-mknc/)

import json
from utils.hot import get_maal, edit_tweet
from utils import *

# env
import os 
from dotenv import load_dotenv
load_dotenv()


# get maal
def synthesize_maal():
    articles_store = read_articles_urls()
    maal = {}
    articles = get_maal(base_urls=articles_store)
    for i in articles:
        maal[i['topic']] = i['content']
    # maal = {
    #     "0": 'nanha ',
    #     "1": 'bada ',
    #     "2": 'pyaara ',
    #     "3": 'chota '
    # }
    return maal

# daily posts
posts = synthesize_maal()

# Update the daily posts
def update_maal():
    global posts
    posts = synthesize_maal()

# Get daily posts
def get_daily_post():
    titles = posts.keys()
    content = "What to post today?"
    for topic in posts:
        content += "\n\nTitle: " + "**" + topic + "**"
        content += "\n\nTweet: " + "`" + posts[topic] + "`"
    return titles, content

# Get selected post
def get_choice(choice):
    post = posts[choice]
    return post

# Function to process the chatbot conversation
def randi_rona(text="", khabar_content=""):
    reply = edit_tweet(
        suggestion = text,
        tweet = khabar_content
    )
    return reply

# Tweet
def submit_post(content):
    try:
        # tweet it
        return f"Tweeted successfully!"
    except Exception as e:
        return f"Some error occurred please select again.\nError: {e}"
    
