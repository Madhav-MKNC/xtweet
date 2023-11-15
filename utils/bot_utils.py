# -*- coding: utf-8 -*-
# author: Madhav Kumar (https://github.com/madhav-mknc/)
# author: Nishant Sharma (https://github.com/sevendaystoglory/)

import json
from utils.hot import get_maal, edit_tweet

# env
import os 
from dotenv import load_dotenv
load_dotenv()


# update articles list
def write_articles_urls(updated_list):
    updated_list = list(set(updated_list))
    with open('.articles_store.json', 'w') as file:
        json.dump(updated_list, file)

# list of articles
def read_articles_urls():
    if not os.path.exists('.articles_store.json'):
        urls = ["https://www.artificialintelligence-news.com/"]
        write_articles_urls(urls)
        return urls
    with open('.articles_store.json', 'r') as file:
        urls = json.load(file)
        if not urls:
            urls = ["https://www.artificialintelligence-news.com/"]
            write_articles_urls(urls)
            return urls

# get maal
def synthesize_maal():
    articles_store = read_articles_urls()
    maal = {}
    for url in articles_store:
        try:
            articles = get_maal(url)
            for i in articles:
                maal[i['topic']] = i['content']
        except Exception as e:
            print(f"[ERROR Fetching {url}]", str(e))
    # maal = {
    #     "0": 'nanha lora',
    #     "1": 'bada lauda',
    #     "2": 'pyaara laura',
    #     "3": 'chota loda'
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
        content += "\n---\n" + topic
        content += "\n---\n" + posts[topic]
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
    