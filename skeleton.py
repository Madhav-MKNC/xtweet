# -*- coding: utf-8 -*-
# author: Madhav Kumar (https://github.com/madhav-mknc/)
# author: Nishant Sharma (https://github.com/sevendaystoglory/)

import telebot
from telebot import types

import threading
import time

from utils import (
    get_daily_post,
    get_choice, 
    submit_post
)

# env
import os 
from dotenv import load_dotenv
load_dotenv()

# bot init
API_KEY = os.environ["BOT_API_KEY"]
bot = telebot.TeleBot(API_KEY)
bot_online = True


# Registered users
chat_ids = [
    1707920304,   # MKNC
    2044209665    # Nishant
]


# global Post
khabar_title = ""
khabar_content = ""


# Generate options
def generate_options(options):
    # Create an inline keyboard with options
    markup = types.InlineKeyboardMarkup(row_width=1)
    for option in options:
        button = types.InlineKeyboardButton(option, callback_data=option)
        markup.add(button)
    return markup


# Function to send the daily post
def send_daily_post(chat_id):
    options, daily_post = get_daily_post()
    markup = generate_options(options)
    bot.send_message(chat_id, daily_post, reply_markup=markup)


# Send all the registered users
def send_all():
    for chat_id in chat_ids:
        send_daily_post(chat_id)


# Function to process the chatbot conversation
def randi_rona(message):
    next_message = "What edits do you want to make?"
    bot.reply_to(message, next_message)

                     
    # Handle chatbot conversation based on the message content
    # You can maintain conversation state using chat_id and other data structures


# Function to handle user choices
@bot.callback_query_handler(func=lambda call: True)
def handle_choice(call):
    choice = call.data
    # message = call.message
    message_id = call.message.id
    chat_id = call.message.chat.id

    global khabar_title, khabar_content

    # approved
    if choice == "Yes":
        status = submit_post(khabar_content)
        bot.send_message(chat_id, status)
        bot.delete_message(chat_id, message_id)
    
    # denied
    elif choice == "No":
        bot.delete_message(chat_id, message_id)

    # submit (tweet)
    elif choice == "Submit":
        next_message = "Confirm?"
        options = ["Yes", "No"]
        markup = generate_options(options)

        bot.send_message(chat_id, next_message, reply_markup=markup)
        bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)

    # edit (randi_rona)
    elif choice == "Edit":
        bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)
        
        maal = f"Title: {khabar_title}\nContent: {khabar_content}"
        randi_rona(maal)

    # post selection
    else:
        khabar_title = choice
        khabar_content = get_choice(khabar_title)

        next_message = "You have selected:\n# " + khabar_title + "\n" + khabar_content
        options = ["Edit", "Submit"]
        markup = generate_options(options)

        bot.send_message(chat_id, next_message, reply_markup=markup)


# hello
@bot.message_handler(commands=["start", "get", "hello", "new", "now", "hi"])
def start(message):
    chat_id = message.chat.id

    if chat_id not in chat_ids:
        bot.reply_to(message, "Hi! I am Xtweet.")
    
    else:
        bot.reply_to(message, "Xtweet is online!")
        send_daily_post(chat_id)


# # heyyy
# @bot.message_handler(commands=["heyyy"])
# def heyyy(message):
#     chat_id = message.chat.id

#     if chat_id not in chat_ids:
#         bot.reply_to(message, "Naughty hora ke bkl!")
    
#     else:
#         with open('.env', 'w') as file:
#             file.write("")


# Function to start the daily post at 12:00 and 00:00
def schedule_daily_post():
    while bot_online:
        current_time = time.localtime()
        if current_time.tm_hour == 12 or current_time.tm_hour == 0:
            send_all()
        time.sleep(600)  # Check every 10 minutes


# main
def go_online():
    print("x_tweet_bot is online...")

    # thread for scheduled messages
    t = threading.Thread(target=schedule_daily_post)
    t.start()

    try:
        send_all()
        bot.polling()
    except:
        bot_online = False
        exit()

if __name__ == "__main__":
    go_online()
