# -*- coding: utf-8 -*-
# author: Madhav Kumar (https://github.com/madhav-mknc/)
# author: Nishant Sharma (https://github.com/sevendaystoglory/)

import telebot

import os 
from dotenv import load_dotenv
load_dotenv()

# api key
API_KEY = os.environ["BOT_API_KEY"]
bot = telebot.TeleBot(API_KEY)


"""
BOT COMMANDS:
/start              => Hello
/update URL_TO_ADD  => Add new url for articles
/get_now            => Get the latest hot/trending topics to post

"""


# enter point
@bot.message_handler(commands=["start"])
def start(x):
    # i am online
    bot.reply_to(x, "Xtweet is online!")


# update url for articles
@bot.message_handler(commands=["update"])
def update(x):
    message = x["text"] # this string includes "/update"
    sender = x["from_user"]["username"]
    bot.reply_to(x, "Updated")


# get content for posting
@bot.message_handler(commands=["get_now"])
def get_now(x):
    message = x["text"] # this string includes "/get_now"
    sender = x["from_user"]["username"]
    bot.reply_to(x, "Akatsuki got it")


# main
def go_online():
    print("x_tweet_bot is online...")
    bot.polling()

if __name__ == "__main__":
    go_online()
