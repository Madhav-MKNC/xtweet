# keep alive server => uptimerobot

from flask import Flask, render_template, jsonify
from threading import Thread
import json

app = Flask('')

@app.route('/')
def home():
    return "Web-server for xtweet bot is online"

@app.route('/logs')
def logs():
    # display logs
    try:
        with open('.logs.txt', 'r') as file:
            data = file.read().strip()
    except Exception as err:
        data = f"[error] {str(err)}"

    return render_template(
        'logs.html', 
        content = data
    )

@app.route('/users_info')
def users_info():
    try:
        with open('.users.json', 'r') as json_file:
            data = json.load(json_file)
            prettified_data = json.dumps(data, indent=4)
        return jsonify(prettified_data)
    except FileNotFoundError:
        return "File not found", 404
    except Exception as err:
        return f"[error] {str(err)}", 500

def run():
    app.run(host='0.0.0.0', port=8000)

def keep_alive():
    t = Thread(target=run)
    t.start()
