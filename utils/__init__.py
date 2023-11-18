# Utilities / helper stuff

import os
import json
from datetime import datetime
import pytz


# Define the timezone for India
india_timezone = pytz.timezone('Asia/Kolkata')

# save logs 
def save_logs(message):
    if not os.path.exists('tmp'):
        os.makedirs('tmp')

    current_ts = datetime.now(india_timezone).strftime("%Y-%m-%d %H:%M:%S")
    log = f"\n[TS]:\t {current_ts}"
    log += f"\n[TEXT]:\t {message.text.strip()}"
    log += f"\n[FROM]:\t ({message.from_user.username}, {message.from_user.first_name} {message.from_user.last_name}, {message.from_user.id})"
    log += f"\n[ON]:\t ({message.chat.title}, {message.chat.username}, {message.chat.first_name} {message.chat.last_name}, {message.chat.id})\n"
    
    with open('tmp/logs.txt', 'a') as file:
        file.write(log)


# update articles list
def write_articles_urls(updated_list):
    updated_list = list(set(updated_list))
    with open('.articles_store.json', 'w') as file:
        json.dump(updated_list, file)

# list of articles
def read_articles_urls():
    DEFAULT_URL = "https://vteam.ai/rss"
    if not os.path.exists('.articles_store.json'):
        urls = [DEFAULT_URL]
        write_articles_urls(urls)
        return urls
    with open('.articles_store.json', 'r') as file:
        urls = json.load(file)
        if not urls:
            urls = [DEFAULT_URL]
            write_articles_urls(urls)
        return urls