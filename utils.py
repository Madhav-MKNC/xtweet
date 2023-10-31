# -*- coding: utf-8 -*-
# author: Madhav Kumar (https://github.com/madhav-mknc/)
# author: Nishant Sharma (https://github.com/sevendaystoglory/)

import openai
from hot import get_maal, edit_tweet

# env
import os 
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.environ['OPENAI_API_KEY']

# daily posts 
def format_maal(og_maal):
    maal = {}
    for i in og_maal:
        maal[i['topic']] = i['content']
    return maal

ARTICLES_PAGE = "https://www.artificialintelligence-news.com/"
maal = get_maal(ARTICLES_PAGE)
posts = format_maal(maal)
# posts = {
#     "0": 'lora',
#     "1": 'lauda',
#     "2": 'laura',
#     "3": 'loda'
# }

# Update the daily posts
def update_maal():
    global posts
    maal = get_maal(ARTICLES_PAGE)
    posts = format_maal(maal)

# Get daily posts
def get_daily_post():
    titles = posts.keys()
    content = "What to post today?"
    for topic in posts:
        content += "\n\n # " + topic
        content += "\n" + posts[topic]
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
        return f"Tweeted successfully!\n\n{content}"
    except Exception as e:
        return f"Some error occurred please select again.\nError: {e}"
    