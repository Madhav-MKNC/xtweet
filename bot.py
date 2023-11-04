# -*- coding: utf-8 -*-
# author: Madhav Kumar (https://github.com/madhav-mknc/)
# author: Nishant Sharma (https://github.com/sevendaystoglory/)

import telebot
from telebot import types

import threading
import time

from utils.bot_utils import (
    get_daily_post,
    get_choice, 
    submit_post,
    randi_rona,
    update_maal
)

from utils.users import (
    users_chat_ids,
    admins_chat_ids, 
    ADMIN_CHAT_ID, 
    save_users
)

# env
import os 
from dotenv import load_dotenv
load_dotenv()

# previous /new hit
previous_generate = time.time()

# bot init
API_KEY = os.environ["BOT_API_KEY"]
bot = telebot.TeleBot(API_KEY)
bot_online = True


# save logs 
def save_logs(message, command="/"):
    if not os.path.exists('tmp'): os.makedirs('tmp')
    with open('tmp/logs.txt', 'a') as file:
        logs = f"\n[{command}] FROM: ({message.from_user.username}, {message.from_user.first_name} {message.from_user.last_name}, {message.from_user.id}) ON: ({message.chat.title}, {message.chat.username}, {message.chat.first_name} {message.chat.last_name}, {message.chat.id})\n"
        file.write(logs)


# Generate options
def generate_options(options):
    # Create an inline keyboard with options
    markup = types.InlineKeyboardMarkup(row_width=1)
    for option in options:
        if len(options) > 30:
            option = option[:30] + "..."
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
    for chat_id in users_chat_ids:
        send_daily_post(chat_id)


# Function to handle user choices
@bot.callback_query_handler(func=lambda call: True)
def handle_choice(call):
    choice = call.data
    message = call.message
    message_id = call.message.id
    chat_id = call.message.chat.id

    global users_chat_ids

    # user ka maamla chal rha hai (posting)
    if choice in ["Yes", "No", "Submit", "Edit"]:
        khabar_title = users_chat_ids[chat_id]['khabar']['title']
        khabar_content = users_chat_ids[chat_id]['khabar']['content']

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

    # admin ka maamla chal rha hai (approve or reject)
    elif choice in ["APPROVE", "REJECT"]:
        requesting_user_id = int(message.text.strip().split()[-1])

        # approve bot access
        if choice == "APPROVE":
            users_chat_ids[requesting_user_id] = {
                "khabar": {
                    "title": "",
                    "content": ""
                }
            }
            save_users(users_chat_ids)
            bot.send_message(requesting_user_id, "Access Granted!")
            bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)
            bot.send_message(chat_id, message.text.replace('Grant access?','Access Granted to:'))

        # reject bot access
        elif choice == "REJECT":
            bot.send_message(requesting_user_id, "Access Rejected!")
            bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)

    # user ka hi maamla chal rha hai (post selection)
    else:
        khabar_title = choice
        khabar_content = get_choice(khabar_title)
        
        # update the new global khabar for the user
        users_chat_ids[chat_id]['khabar']['title'] = khabar_title
        users_chat_ids[chat_id]['khabar']['content'] = khabar_content

        next_message = "You have selected:\n# " + khabar_title + "\n" + khabar_content
        options = ["Edit", "Submit"]
        markup = generate_options(options)

        bot.send_message(chat_id, next_message, reply_markup=markup)


# COMMANDS
"""
For general users:
/start          ==> entry point (other commands: /hello, /hi, /help)
/login          ==> for bot access

For registered users:
/get            ==> get hot posts to tweet
/new            ==> update the maal
/edit           ==> make suggestions in the post content
/tweet          ==> tweet a manually edited post
# /auth           ==> authenticate twitter for posting tweets

For admin users:
/remove         ==> remove a user
# /add_url        ==> add new articles url
# /heyyy          ==> hot secret command
"""


# hello (general users)
@bot.message_handler(commands=["start", "hello", "hi", "help"])
def start(message):
    # save logs
    save_logs(message, command="/start")

    chat_id = message.chat.id
    
    if chat_id in admins_chat_ids:
        INFO = "Hello! I am Xtweet.\n\n/start - This message\n/login - For access\n/tweet - For manually written tweets\n/get - For generating hot tweets\n/new - For updating hot tweets\n/remove USER_ID - For deleting a user"

    else:
        INFO = "Hello! I am Xtweet.\n\n/start - This message\n/login - For access\n/tweet - For manually written tweets\n/get - For generating hot tweets\n/new - For updating hot tweets"

    bot.reply_to(message, INFO)


# login (GENERAL USERS)
@bot.message_handler(commands=["login"])
def login(message):
    user_id = message.from_user.id

    if user_id in users_chat_ids:
        return 

    user_username = message.from_user.username
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name

    next_message = f"Grant access?\nusername: {user_username}\nfirst name: {user_first_name}\nlast name: {user_last_name}\nuser id: {user_id}" # don't change it (see "elif 'APPROVE'" code) 
    options = ["APPROVE", "REJECT"]
    markup = generate_options(options)

    for admin in admins_chat_ids[0:1]:
        bot.send_message(admin, next_message, reply_markup=markup)


# get (REGISTERED USERS)
@bot.message_handler(commands=["get"])
def get(message):
    chat_id = message.chat.id

    if chat_id not in users_chat_ids:
        return
    
    send_daily_post(chat_id)


# new (REGISTERED USERS)
@bot.message_handler(commands=["new"])
def new(message):
    chat_id = message.chat.id

    if chat_id not in users_chat_ids:
        return
    
    if time.time() - previous_generate < 100:
        bot.reply_to(message, "Generating...")
        return
    
    bot.reply_to(message, "Generating... might take a minute")
    update_maal()
    previous_generate = time.time()
    send_daily_post(chat_id)


# edit (REGISTERED USERS)
@bot.message_handler(commands=["edit"])
def edit(message):
    chat_id = message.chat.id
    text = message.text[5:].strip()

    global users_chat_ids
    khabar_content = users_chat_ids[chat_id]['khabar']['content']

    if not text or chat_id not in users_chat_ids:
        return 

    khabar_content = randi_rona(text=text, khabar_content=khabar_content)
    users_chat_ids[chat_id]['khabar']['content'] = khabar_content
    bot.reply_to(message, khabar_content)

    next_message = "Confirm?"
    options = ["Yes", "No"]
    markup = generate_options(options)

    bot.send_message(chat_id, next_message, reply_markup=markup)


# tweet (REGISTERED USERS)
@bot.message_handler(commands=["tweet"])
def tweet(message):
    chat_id = message.chat.id
    text = message.text[6:].strip()

    global users_chat_ids

    if not text or chat_id not in users_chat_ids:
        return
    
    users_chat_ids[chat_id]['khabar']['content'] = text

    next_message = "You have selected:\n" + text
    options = ["Edit", "Submit"]
    markup = generate_options(options)

    bot.send_message(chat_id, next_message, reply_markup=markup)


# # authenticate twitter (REGISTERED USERS)
# @bot.message_handler(commands=["auth"])
# def auth(message):
#     chat_id = message.chat.id
#     text = message.text[5:].strip()

#     if not text or chat_id not in users_chat_ids:
#         return
    
#     bot.reply_to(message, "[feature under construction]")


# # add new url for articles (ADMIN USERS)
# @bot.message_handler(commands=["add_url"])
# def add_url(message):
#     chat_id = message.chat.id

#     if chat_id not in admins_chat_ids:
#         return 
    
#     bot.reply_to(message, "add url!")


# remove a registered user (ADMIN USERS)
@bot.message_handler(commands=["remove"])
def remove(message):
    chat_id = message.chat.id
    text = message.text[7:].strip() # this should be user id of the user to be deleted

    if chat_id not in admins_chat_ids[0:1]:
        return 
    
    try:
        global users_chat_ids
        user_id = int(text)
        users_chat_ids.pop(user_id)
        save_users(users_chat_ids)
        bot.reply_to(message, f"Deleted user_id:{user_id}")
        bot.send_message(user_id, "Your access has been terminated!")
    except Exception as e:
        bot.reply_to(message, f"Some error while deleting a user, error: {e}")

    
# # heyyy (ADMIN USERS)
# @bot.message_handler(commands=["heyyy"])
# def heyyy(message):
#     chat_id = message.chat.id

#     if chat_id not in admins_chat_ids:
#         return 
    
#     bot.reply_to(message, "heyyy!")


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
