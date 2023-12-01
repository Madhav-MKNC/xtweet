# Registered users

import json
import os

#  admin group
ADMIN_CHAT_ID = -4041790014

# admin users
admins_chat_ids = [
    -4041790014,    # Xtweet Admins (group)
    1707920304,     # MKNC
    2044209665      # Nishant
]

# save data locally
def save_users(users_dict):
    with open('.users.json', 'w') as file:
        json.dump(users_dict, file)

# get users 
def load_users():
    DEFAULT = {}

    if not os.path.exists(".users.json"):
        with open(".users.json") as file:
            file.write(str(DEFAULT))

    with open('.users.json', 'r') as file:
        users_dict = json.load(file)
        users_dict = {int(k): v for k, v in users_dict.items()}

    return users_dict

# general users
users_chat_ids = load_users()
