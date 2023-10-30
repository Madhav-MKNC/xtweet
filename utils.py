# -*- coding: utf-8 -*-
# author: Madhav Kumar (https://github.com/madhav-mknc/)
# author: Nishant Sharma (https://github.com/sevendaystoglory/)

import os
import requests

import openai



# env
import os 
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.environ['OPENAI_API_KEY']

# daily posts 
# 
posts = {
    "0": 'lora',
    "1": 'lauda',
    "2": 'laura',
    "3": 'loda'
}


def get_new_stuff():
    global posts
    # 
    posts = {
        "0": 'lora',
        "1": 'lauda',
        "2": 'laura',
        "3": 'loda'
    }


def get_daily_post():
    titles = posts.keys()
    content = "What to post today?"
    for topic in posts:
        content += "\n\n # " + topic
        content += "\n" + posts[topic]

    return titles, content


def get_choice(choice):
    post = posts[choice]
    return post


def submit_post(content):
    try:
        # tweet it
        return f"Tweeted successfully!\n\n{content}"
    except Exception as e:
        return f"Some error occurred please select again.\nError: {e}"


# Function to process the chatbot conversation
def randi_rona(text="", khabar_content=""):
    prompt = [
        {
            'role' : 'system', 
            'content' : "You will be given a certain tweet. You are to enchance minimally the content as per the instrcutions provided by the user. Output only the final edited tweet and nothing else, for any exceptions you will output the same tweet. The user prompt will look like.\n\nTweet: {content of the tweet}\nInstruction: {user instructions}."
        },
        {
            'role': 'user',
            'content': f"Tweet: {khabar_content}\nInstruction: {text}"
        }
    ]
    print('prompt aagaya')

    response = openai.ChatCompletion.create(
        messages = prompt,
        model = "gpt-4",
        temperature = 0.3,
    )
    print('response aa gya malaidaar')

    reply = response.choices[0]['message']['content']
    return reply
