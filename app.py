import re
from flask import Flask, request
import telegram
from telebot.credentials import BOT_TOKEN, BOT_USER_NAME, BOT_URL
from telebot.engine import Engine, State

global bot
global TOKEN
TOKEN = BOT_TOKEN
bot = telegram.Bot(token=TOKEN)
engine = Engine()

app = Flask(__name__)

def send(chat_id, state, value):
    try:
        if state == State.TEXT:
            bot.sendMessage(chat_id=chat_id, text=value)
        elif state == State.PHOTO:
            bot.sendPhoto(chat_id=chat_id, photo=value)
        else:
            bot.sendMessage(chat_id=chat_id, text=value)
    except:
        bot.sendMessage(chat_id=chat_id, text='Coś poszło nie tak :(')


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    text = update.message.text.encode('utf-8').decode()
    text = text.lower()

    if text == "/start":
            answer = engine.get_welcome()
    elif text[:6] == "/pomoc":
            answer = engine.get_help()
    elif text[:6] == "/wiki ":
            answer = engine.get_wikipedia(text[5:])
    elif text[:4] == '/tr ':
        answer = engine.get_translator(text[4:], 'pl')
    elif text[:5] == '/tra ':
        answer = engine.get_translator(text[5:], 'en')
    elif text[:4] == '/yt ':
        answer = engine.get_youtube(text[4:])
    elif text[:8] == '/pogoda ':
        answer = engine.get_weather(text[8:])
    else:
            answer = engine.get_answer(chat_id, text)      

    for state, value in answer:
        send(chat_id, state, value)

    return ''

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return '.'


if __name__ == '__main__':
    app.run(threaded=True)