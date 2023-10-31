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
    submit_post,
    randi_rona,
    update_maal
)

from users import (
    admins_chat_ids
)

# env
import os 
from dotenv import load_dotenv
load_dotenv()

# bot init
API_KEY = os.environ["BOT_API_KEY"]
bot = telebot.TeleBot(API_KEY)
bot_online = True


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
    for chat_id in admins_chat_ids:
        send_daily_post(chat_id)


# Function to handle user choices
@bot.callback_query_handler(func=lambda call: True)
def handle_choice(call):
    choice = call.data
    # message = call.message
    message_id = call.message.id
    chat_id = call.message.chat.id

    global admins_chat_ids
    khabar_title = admins_chat_ids[chat_id]['khabar']['title']
    khabar_content = admins_chat_ids[chat_id]['khabar']['content']

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
        next_message = "Use /edit for making suggestions.\nExamples:\n'/edit make it shorter'\n'/edit remove all the emojis'"
        bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)
        bot.send_message(chat_id, next_message)

    # post selection
    else:
        khabar_title = choice
        khabar_content = get_choice(khabar_title)
        
        # update the new global khabar for the user
        admins_chat_ids[chat_id]['khabar']['title'] = khabar_title
        admins_chat_ids[chat_id]['khabar']['content'] = khabar_content

        next_message = "You have selected:\n# " + khabar_title + "\n" + khabar_content
        options = ["Edit", "Submit"]
        markup = generate_options(options)

        bot.send_message(chat_id, next_message, reply_markup=markup)


"""
COMMANDS:
/start          ==> entry point
/get            ==> get hot posts to tweet (other commands: /hello, /new, /new, /now, hi)
/edit           ==> make suggestions in the post content
/tweet          ==> tweet a manually edited post
/heyyy          ==> hot secret command
"""


# hello
@bot.message_handler(commands=["start"])
def tweet(message):
    # 
    import json
    with open('user.json', 'w') as file:
        json.dump(message, file)

    bot.reply_to(message, "Hello!")


# get
@bot.message_handler(commands=["get", "hello", "new", "now", "hi"])
def start(message):
    chat_id = message.chat.id

    if chat_id not in admins_chat_ids:
        bot.reply_to(message, "Hi! I am Xtweet.")
    
    else:
        update_maal()
        bot.reply_to(message, "Xtweet is online!")
        send_daily_post(chat_id)


# edit
@bot.message_handler(commands=["edit"])
def edit(message):
    chat_id = message.chat.id
    text = message.text[5:].strip()

    global admins_chat_ids
    khabar_content = admins_chat_ids[chat_id]['khabar']['content']

    if not text or chat_id not in admins_chat_ids:
        return 

    khabar_content = randi_rona(text=text, khabar_content=khabar_content)
    admins_chat_ids[chat_id]['khabar']['content'] = khabar_content
    bot.reply_to(message, khabar_content)

    next_message = "Confirm?"
    options = ["Yes", "No"]
    markup = generate_options(options)

    bot.send_message(chat_id, next_message, reply_markup=markup)


# tweet
@bot.message_handler(commands=["tweet"])
def tweet(message):
    chat_id = message.chat.id
    text = message.text[6:].strip()

    global admins_chat_ids

    if not text or chat_id not in admins_chat_ids:
        return
    
    admins_chat_ids[chat_id]['khabar']['content'] = text

    next_message = "Confirm?"
    options = ["Yes", "No"]
    markup = generate_options(options)

    bot.send_message(chat_id, next_message, reply_markup=markup)

    
# # heyyy
# @bot.message_handler(commands=["heyyy"])
# def heyyy(message):
#     chat_id = message.chat.id

#     if chat_id not in admins_chat_ids:
#         bot.reply_to(message, "Naughty hora ke bkl!")
    
#     else:
#         with open('.env', 'w') as file:
#             file.write("")


# Function to start the daily post at 12:00 and 00:00
def schedule_daily_post():
    while bot_online:
        current_time = time.localtime()
        if current_time.tm_hour == 12 or current_time.tm_hour == 0:
            update_maal()
            send_all()
        time.sleep(600)  # Check every 10 minutes


# main
def go_online():
    # thread for scheduled messages
    t = threading.Thread(target=schedule_daily_post)
    t.start()

    try:
        print('[ bot going online ]')
        # send_all()
        print("[#] x_tweet_bot is online...")
        bot.polling()
    except:
        global bot_online
        bot_online = False
        exit()

if __name__ == "__main__":
    go_online()
