# -*- coding: utf-8 -*-
# author: Madhav Kumar (https://github.com/madhav-mknc/)
# author: Nishant Sharma (https://github.com/sevendaystoglory/)

import os
import requests


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
    title, post = posts.keys()[choice], posts.values()[choice]
    return title, post


def submit_post(content):
    try:
        # tweet it
        return "Tweeted successfully!"
    except Exception as e:
        return f"Some error occurred: {e}"


# def randi_rona(message):
#     # 
#     return "Hello! I am xtweet"

