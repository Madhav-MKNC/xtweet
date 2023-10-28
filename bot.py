# -*- coding: utf-8 -*-
# author: Madhav Kumar (https://github.com/madhav-mknc/)
# author: Nishant Sharma (https://github.com/sevendaystoglory/)

import telebot
import datetime

import os 
from dotenv import load_dotenv
load_dotenv()

# api key
API_KEY = os.environ["API_KEY"]
bot = telebot.TeleBot(API_KEY)


def get_get():
  with open('time.txt', 'r') as file:
    starting_time = list(map(int, file.read().split()))
  current_time = list(
    map(int,
        datetime.datetime.now().strftime("%d %H").split()))
  Time = starting_time[1] + 6 if starting_time[
    1] < 18 else starting_time[1] - 18
  if starting_time[1] < 18:
    day, Time = starting_time[0], starting_time[1] + 6
  else:
    day, Time = starting_time[0] + 1, starting_time[1] - 18

  streak = (current_time[0] -
            starting_time[0]) * 24 + current_time[1] - starting_time[1]
  text = f"""
Your Streak: /get

    >> {streak} hours
    >> {streak//24} Days {streak%24} hours
    
    Beginned on {day} at {Time}:00

All commands:\n\n/get\n\n/highest\n\n/now\n\n/reset dd hh
    """
  return streak, text


def highest():  #
  with open("best.txt", "r") as b:
    maxx = int(b.read())
  current = get_get()[0]
  if current >= maxx:
    maxx = current
    with open("best.txt", 'w') as b:
      b.write(str(maxx))
  return maxx


def changetime(time):
  # time[1] += 6
  with open('time.txt', 'w') as file:
    file.write(" ".join(map(str, time)))


@bot.message_handler(commands=["now"])
def now(x):
  starting_time = list(
    map(int,
        datetime.datetime.now().strftime("%d %H").split()))
  bot.reply_to(
    x, "RESET DONE\n\ncommands:\n\n/get\n\n/highest\n\n/now\n\n/reset dd hh")
  print("init time reset [+]")
  changetime(starting_time)


@bot.message_handler(commands=["reset"])
def reset(x):
  reply_text = ""
  try:
    inp = list(map(int, x.text.split()[1:]))
    print(inp)
    if inp[0] not in range(1, 32): raise "Invalid Date"
    elif inp[1] not in range(1, 25): raise "Invalid hour"
    if inp[1] <= 6:
      inp[0] -= 1
      inp[1] += 24
    inp[1] -= 6
    starting_time = inp
    changetime(starting_time)
    reply_text = "RESET DONE"
  except:
    # changetime([15, 5])
    reply_text = "Command: /reset dd hh"
  reply_text += "\n\ncommands:\n\n/get\n\n/highest\n\n/now\n\n/reset dd hh"
  bot.reply_to(x, reply_text)


@bot.message_handler(commands=["get", "start"])
def get(x):
  text = get_get()[1]
  # print(current_time, starting_time)
  bot.reply_to(x, text)


@bot.message_handler(commands=["highest"])
def best(x):
  longest = highest()
  bot.reply_to(
    x,
    f"The longest streak: {longest} Hours\nor\n{longest//24} Days {longest%24} hours long"
  )


def online():
  print("Timer Bot is online...")
  bot.polling()