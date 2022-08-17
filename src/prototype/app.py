import random

from flask import Flask, request
# from mailer import Mailer
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import random
import smtplib

gmail_user = 'iiepe6op@gmail.com'
gmail_password = 'aarkahldsqizguga'


# username = 'janiecee'
postfixMail = '@student.21-school.ru'

def sendEmail(gmail_user, username):
    rndFour = random.randint(1000, 9999)
    sent_from = gmail_user
    to = username + postfixMail
    subject = 'CODE VOTEBOT'
    body = str(rndFour)
    print(gmail_user, rndFour, to)
    email_text = body
    print(email_text)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
    except:
        print('Something went wrong...')
    return body

TOKEN_API = '639642745:AAHd9aIHomuZZH7-pxJPRpWAAdMjF4vHRWc'

bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot)
storage = MemoryStorage()

button1 = KeyboardButton('/username')
button2 = KeyboardButton('/info')
button5 = KeyboardButton('/poll')
keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(button1, button2, button5)

button3 = KeyboardButton('Who are you?', request_contact=True)
button4 = KeyboardButton('Where are you?', request_location=True)
keyboard2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(button3, button4)

app = Flask(__name__)

class Form(StatesGroup):
    username = State()

@dp.message_handler(commands=["poll"])
async def cmd_start(message: types.Message):
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text="Quize",
                                           request_poll=types.KeyboardButtonPollType(type=types.PollType.QUIZ)))
    poll_keyboard.add(types.KeyboardButton(text="Regular",
                                           request_poll=types.KeyboardButtonPollType(type=types.PollType.REGULAR)))
    poll_keyboard.add(types.KeyboardButton(text="Mode",
                                           request_poll=types.KeyboardButtonPollType(type=types.PollType.mode)))
    poll_keyboard.add(types.KeyboardButton(text="/cancel"))
    if message.text == 'Cancel':
        await message.answer("/cancel", reply_markup=keyboard1)
        return
    await message.answer("Create new poll", reply_markup=poll_keyboard)

@dp.message_handler(content_types=["poll"])
async def msg_with_poll(message: types.Message):
    # Если юзер раньше не присылал запросы, выделяем под него запись
    if not quizzes_database.get(str(message.from_user.id)):
        quizzes_database[str(message.from_user.id)] = []

    # If user don't have ADMIN permission -
    if message.poll.type != "quiz":
        await message.reply("Sorry, only ADMIN")
        return

    # Сохраняем себе викторину в память
    quizzes_database[str(message.from_user.id)].append(Quiz(
        poll_id=message.poll.id,
        question=message.poll.question,
        options=[o.text for o in message.poll.options],
        # if message.poll.type == "quiz":
        correct_option_id=message.poll.correct_option_id,
        owner_id=message.from_user.id)
    )
    # Сохраняем информацию о её владельце для быстрого поиска в дальнейшем
    quizzes_owners[message.poll.id] = str(message.from_user.id)

    await message.reply(f'Викторина сохранена. Общее число сохранённых викторин: {len(quizzes_database[str(message.from_user.id)])}')

@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    """Conversation entrypoint"""
    # Set state
    await Form.username.set()
    await message.reply("Send me your name", reply_markup=keyboard1)

@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    await message.reply('Contact and location', reply_markup=keyboard2)

@dp.message_handler(commands=['cancel'])
async def menu(message: types.Message):
    await message.reply("Menu", reply_markup=keyboard1)


# @dp.message_handler()
# async def kb_answer(message: types.Message):
#     if message.text == 'Enter username':
#         print('name enter!')
#         if message.answer(message.text) != '' :
#             @dp.callback_query_handler(text=[{message.text}])
#             async def enterCode(call: types.CallbackQuery):
#                 rndFour = sendEmail(gmail_user, username)
#                 await message.answer('Enter CODE from email')
#                 @dp.callback_query_handler(text=[str(rndFour)])
#                 async def checkCode(call: types.CallbackQuery):
#                     if message.text == str(rndFour):
#                         await message.answer('SUCCESS!')
#                     else:
#                         await message.answer(f'CODE: {message.text} WRONG, TRY AGAIN!')

@dp.message_handler(state=Form.username)
async def process_name(message: types.Message, state: FSMContext):
    """Process user name"""
    # Finish our conversation
    username = {message.text}
    rndFour = sendEmail(gmail_user, username)
    await state.finish()
    await message.reply(f"Hello, {message.text}")
    if code == str(rndFour):
        await message.reply("/poll")

# @dp.message_handler(commands=['username'])
# async def add_username_to_db(message: types.Message):
#     # if message.text == 'Enter username':
#     # message.reply_to_message is a types.Message object too
#     try:
#         username = message.reply_to_message.text
#         if username: # if replied
#             rndFour = sendEmail(gmail_user, username)
#     except AttributeError:
#         username = 'not replied'
#     try:
#         code = message.reply_to_message.text  # if replied
#         if code == str(rndFour):
#             await message.reply("/poll")
#     except AttributeError:
#         code = 'not replied'
    # await message.answer(f'Replied message text: {username, code}')
    # await message.answer(f'Message text: {message.text}')

executor.start_polling(dp)
