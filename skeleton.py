# -*- coding: utf-8 -*-
# author: Madhav Kumar (https://github.com/madhav-mknc/)
# author: Nishant Sharma (https://github.com/sevendaystoglory/)

import telebot
from telebot import types
import time

from utils import (
    get_daily_post,
    get_choice, 
    submit_post, 
    randi_rona
)

# env
import os 
from dotenv import load_dotenv
load_dotenv()

# bot init
API_KEY = os.environ["BOT_API_KEY"]
bot = telebot.TeleBot(API_KEY)


# Function to send the daily post
def send_daily_post(chat_id):
    # Generate the daily post using your get_daily_post() function
    daily_post = get_daily_post()

    # Create an inline keyboard with options
    markup = types.InlineKeyboardMarkup(row_width=1)
    options = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]

    for option in options:
        button = types.InlineKeyboardButton(option, callback_data=option)
        markup.add(button)

    # Send the daily post with options
    bot.send_message(chat_id, daily_post, reply_markup=markup)

# Function to handle user choices
@bot.callback_query_handler(func=lambda call: True)
def handle_choice(call):
    choice = call.data
    chat_id = call.message.chat.id

    # Generate the next message using your get_choice() function
    next_message = get_choice(choice)

    # Send the next message
    bot.send_message(chat_id, next_message)

# Function to handle the "final submit" or "edit" options
@bot.message_handler(commands=['final_submit', 'edit'])
def handle_final_submit(message):
    chat_id = message.chat.id
    command = message.text

    if command == '/final_submit':
        # Call your submit_post() function
        submit_post()
    elif command == '/edit':
        # Start a conversation with the chatbot
        bot.send_message(chat_id, "Editing your post. Please proceed with your changes.")
        randi_rona(message)  # Use the alias here

# Function to process the chatbot conversation
def chatbot(message):
    # Your chatbot logic goes here
    # You can use the message.chat.id to keep track of the conversation state

    # Example:
    chat_id = message.chat.id

    # Handle chatbot conversation based on the message content
    # You can maintain conversation state using chat_id and other data structures

# Function to start the daily post at 12:00 and 00:00
def schedule_daily_post():
    chat_id = '1707920304'  # Replace with your chat ID
    while True:
        current_time = time.localtime()
        if current_time.tm_hour == 12 or current_time.tm_hour == 0:
            send_daily_post(chat_id)
        time.sleep(60)  # Check every minute

if __name__ == '__main__':
    # Start a thread to schedule daily posts
    import threading
    t = threading.Thread(target=schedule_daily_post)
    t.start()

    # Start the bot
    send_daily_post('1707920304')
    bot.polling()