import random

from flask import Flask, request
from mailer import Mailer
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import random
# from trycourier import Courier
#
# client = Courier(auth_token="pk_prod_J75GGW0Y4ZM2JZNQQ1ZCZY6FFRQC")
#
# resp = client.send_message(
#   message={
#     "to": { "antinlay@gmail.com"
#     },
#     "template": "KY0RJ1CHC746TGQJKBJW4HBD43CK",
#     "data": {
#       "variables": "awesomeness",
#     },
#   }
# )
#
# print(resp['requestId'])

TOKEN_API = '639642745:AAHd9aIHomuZZH7-pxJPRpWAAdMjF4vHRWc'

postfixMail = '@student.21-school.ru'


bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot)

button1 = KeyboardButton('Enter username')
button2 = KeyboardButton('Coins')
keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(button1, button2)

button3 = KeyboardButton('Who are you?', request_contact=True)
button4 = KeyboardButton('Where are you?', request_location=True)
keyboard2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(button3, button4)

app = Flask(__name__)

# mail = Mailer(email='iiepe6op@gmail.com', password='3Bx6G7O3')
# mail.send(receiver='janiecee@student.21-school.ru', subject='CODE', message=str(rndFour))

@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
    await message.reply("Privet. Kak tvoi dela?", reply_markup=keyboard1)

# @dp.message_handler(commands=['info'])
# async def info(message: types.):
#     await

@dp.message_handler()
async def kb_answer(message: types.Message, ):
    if message.text == 'Enter username':
        await message.answer('How are you?')
    elif message.text == 'Coins':
        await message.answer('100000 00 0000021')
    else:
        await message.answer(f'Your message is: {message.text}')

executor.start_polling(dp)

# def send_message(chat_id, text):
#     method = "sendMessage"
#     url = f"https://api.telegram.org/bot{TOKEN_API}/{method}"
#     data = {"chat_id": chat_id, "text": text}
#     requests.post(url, data=data)
#
# @app.route("/", methods=["GET", "POST"])
# def receive_update():
#     if request.method == "POST":
#         print(request.json)
#         chat_id = request.json["message"]["chat"]["id"]
#         send_message(chat_id, "Privet El'vina. Kak tvoi dela?")
#     return {"ok": True}

# @app.route('/', methods=["POST"])
# def process():  # put application's code here
#     print(request.json)
#     return {"ok": True}

# if __name__ == '__main__':
#     app.run()
