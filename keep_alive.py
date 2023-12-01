# keep alive server => uptimerobot

from flask import Flask, render_template
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Web-server for xtweet bot is online"

@app.route('/logs')
def logs():
    # display logs
    try:
        with open('.logs.txt', 'r') as file:
            display = file.read().strip()
    except Exception as err:
        display = f"[error] {str(err)}"

    return render_template(
        'logs.html', 
        content = display
    )

def run():
    app.run(host='0.0.0.0', port=8000)

def keep_alive():
    t = Thread(target=run)
    t.start()
