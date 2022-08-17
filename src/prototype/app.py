import random

from flask import Flask, request
# from mailer import Mailer
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import random
import smtplib

rndFour = random.randint(1000, 9999)

gmail_user = 'iiepe6op@gmail.com'
gmail_password = 'aarkahldsqizguga'


username = 'antinlay'

def sendEmail(gmail_user, rndFour, username):
    sent_from = gmail_user
    to = [username + '@gmail.com']
    subject = 'CODE VOTEBOT'
    body = str(rndFour)

    email_text = """\
    From: %s
    To: %s
    Subject: %s
    
    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
    except:
        print('Something went wrong...')
        return 0


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


# mail = Mailer(email='iiepe6op@gmail.com', password='aarkahldsqizguga')
# mail = Mailer.login(usr='iiepe6op@gmail.com', pwd='aarkahldsqizguga')
# mail.send(receiver='janiecee@student.21-school.ru', subject='CODE', message=str(rndFour))

@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
    await message.reply("Privet. Kak tvoi dela?", reply_markup=keyboard1)


@dp.message_handler()
async def kb_answer(message: types.Message):
    if message.text == 'Enter username':
        sendEmail(gmail_user, rndFour, username)
        # await message.answer('Enter CODE from email')
    elif message.text == str(rndFour):
        await message.answer('SUCCESS!')
    else:
        await message.answer(f'CODE: {message.text} WRONG, TRY AGAIN!')


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
