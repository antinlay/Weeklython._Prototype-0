import logging

from models import db, User, City

from flask import Flask, request

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import aiogram.utils.markdown as md
import random
import smtplib

logging.basicConfig(level=logging.INFO)

TOKEN_API = '5595416871:AAEgo1_AqnHMqbWemI8fPplxy3n2pbqcXy0'

bot = Bot(token=TOKEN_API)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

gmail_user = 'iiepe6op@gmail.com'
gmail_password = 'aarkahldsqizguga'


# username = 'janiecee'
# postfixMail = '@student.21-school.ru'
# adminMail = '@21-school.ru'

def sendEmail(gmail_user, username, postfixMail):
    rndFour = random.randint(1000, 9999)
    sent_from = gmail_user
    to = username + postfixMail
    # subject = 'CODE VOTEBOT'
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

buttonStudent = KeyboardButton('/student')
buttonAdmin = KeyboardButton('/adm')

buttonUsername = KeyboardButton('/username')
buttonInfo = KeyboardButton('/info')
buttonPoll = KeyboardButton('/poll')
buttonCreatePoll = KeyboardButton('/create_poll')
keyboardPoll = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(buttonInfo, buttonPoll)
keyboardCreatePoll = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(buttonInfo, buttonCreatePoll)

button3 = KeyboardButton('Who are you?', request_contact=True)
button4 = KeyboardButton('Where are you?', request_location=True)
keyboard2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(button3, button4)

buttonCampus1 = KeyboardButton('Kazan')
buttonCampus2 = KeyboardButton('Moscow')
buttonCampus3 = KeyboardButton('Novosibirsk')
keyboardCampus = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(buttonCampus1, buttonCampus2, buttonCampus3)

buttonWave1 = KeyboardButton('w12')
buttonWave2 = KeyboardButton('w13')
buttonWave3 = KeyboardButton('w14')
keyboardWave = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(buttonWave1, buttonWave2, buttonWave3)

buttonTribe1 = KeyboardButton('ignis')
buttonTribe2 = KeyboardButton('aqua')
buttonTribe3 = KeyboardButton('air')
buttonTribe4 = KeyboardButton('terra')
keyboardTribe = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(buttonTribe1, buttonTribe2, buttonTribe3, buttonTribe4)

keyboardRole = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(buttonStudent, buttonAdmin)


app = Flask(__name__)
db.create_all()

# city = City(city_name='Kazan')
# db.session.add(city)
# db.session.commit()

class Form(StatesGroup):
    role = State()
    username = State()
    code = State()
    wave = State()
    tribe = State()
    campus = State()

@dp.message_handler(commands=['help', 'start'])
async def start(message: types.Message):
    await Form.role.set()
    await message.answer("Choose role:", reply_markup=keyboardRole)

@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)
    await state.finish()
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(lambda message: message.text not in ["/adm", "/student"], state=Form.role)
async def checkRole(message: types.Message):
    return await message.reply("Bad role. Choose your role from the keyboard.")
@dp.message_handler(state=Form.role)
async def saveRole(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['role'] = message.text
        print(data['role'])
    await Form.next()
    curUser = message.from_user.id
    nameUser = message.from_user.username
    user = User.query.filter_by(user_id=curUser).first()
    if user is None:
        await Form.username.set()
        await message.reply("Send me username:")
    else:
        if data['role'] == "/adm":
            await message.answer(f'Welcome back, ' + str(nameUser), reply_markup=keyboardCreatePoll)
        elif data['role'] == "/student":
            await message.answer(f'Welcome back, ' + str(nameUser), reply_markup=keyboardPoll)

# @dp.message_handler(commands=['adm'])
# async def cmdAdm(message: types.Message):
#     """Conversation entrypoint"""
#     curUser = message.from_user.id
#     nameUser = message.from_user.username
#     user = User.query.filter_by(user_id=curUser).first()
#     if user is None:
#         await Form.username.set()
#         await message.reply("Send me username:")
#     else:
#         await message.answer(f'Welcome back, ' + str(nameUser), reply_markup=keyboardCreatePoll)
#
#
# @dp.message_handler(commands=['student'])
# async def cmdStudent(message: types.Message):
#     """Conversation entrypoint"""
#     curUser = message.from_user.id
#     nameUser = message.from_user.username
#     user = User.query.filter_by(user_id=curUser).first()
#     if user is None:
#         await Form.username.set()
#         await message.reply("Send me username:")
#     else:
#         await message.answer(f'Welcome back, ' + str(nameUser), reply_markup=keyboardPoll)

@dp.message_handler(state=Form.username)
async def sendUsername(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text
    if data['role'] == '/adm':
        postfixMail = '@21-school.ru'
    elif data['role'] == '/student':
        postfixMail = '@student.21-school.ru'
    else:
        return
    await message.reply('Enter code from your email ' + data['username'] + postfixMail + ':')
    code = sendEmail(gmail_user, data['username'], postfixMail)
    await Form.next()
    @dp.message_handler(lambda message: not message.text.isdigit(), state=Form.code)
    async def checkCode(message: types.Message):
        return await message.reply('Code is WRONG.\nTry again:')

    @dp.message_handler(state=Form.code)
    async def processCode(message: types.Message, state: FSMContext):
        if str(code) == message.text:
            await Form.next()
            await state.update_data(code=int(message.text))
            await message.answer("All right!\nChoose your wave:", reply_markup=keyboardWave)
        else:
            return await message.reply('Code is WRONG.\nTry again:')

@dp.message_handler(lambda message: message.text not in ["w12", "w13", "w14"], state=Form.wave)
async def checkWave(message: types.Message):
    return await message.reply("Bad wave. Choose your wave from the keyboard.")

@dp.message_handler(state=Form.wave)
async def processWave(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['wave'] = message.text
    await Form.next()
    await message.answer("All right!\nChoose your wave:", reply_markup=keyboardTribe)

@dp.message_handler(lambda message: message.text not in ["ignis", "aqua", "air", "terra"], state=Form.tribe)
async def checkTribe(message: types.Message):
    return await message.reply("Bad tribe. Choose your tribe from the keyboard.")

@dp.message_handler(state=Form.tribe)
async def processTribe(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tribe'] = message.text
    await Form.next()
    await message.answer("All right!\nChoose your campus:", reply_markup=keyboardCampus)

@dp.message_handler(lambda message: message.text not in ["Kazan", "Moscow", "Novosibirsk"], state=Form.campus)
async def checkCampus(message: types.Message):
    return await message.reply("Bad campus. Choose your campus from the keyboard.")

@dp.message_handler(state=Form.campus)
async def processCampus(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['campus'] = message.text

        markup = types.ReplyKeyboardRemove()
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Hello ', md.bold(data['username'])),
                md.text('Campus: ', md.bold(data['campus'])),
                sep='\n',
            ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )
    curUser = message.from_user
    newUser = User(user_id=curUser.id, telegram_username=curUser.username, platform_username=data['username'], city_id=data['campus'])
    db.session.add(newUser)
    db.session.commit()
    await state.finish()
    await message.answer('You have Admin permissions. Now you can create and reply poll', reply_markup=keyboardCreatePoll)
@dp.message_handler(commands=["create_poll"])
async def cmd_start(message: types.Message):
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # poll_keyboard.add(types.KeyboardButton(text="Quize",
    #                                        request_poll=types.KeyboardButtonPollType(type=types.PollType.QUIZ)))
    # poll_keyboard.add(types.KeyboardButton(text="Regular",
    #                                        request_poll=types.KeyboardButtonPollType(type=types.PollType.REGULAR)))
    poll_keyboard.add(types.KeyboardButton(text="Mode",
                                           request_poll=types.KeyboardButtonPollType(type=types.PollType.mode)))
    poll_keyboard.add(types.KeyboardButton(text="/cancel"))
    # if message.text == "Cancel":
    #     markup = types.ReplyKeyboardRemove()
    #     await message.answer('cancel', reply_markup=markup)
    #     return
    await message.answer("Create new poll", reply_markup=poll_keyboard)

# @dp.message_handler(content_types=["poll"])
# async def msg_with_poll(message: types.Message):
#     # Если юзер раньше не присылал запросы, выделяем под него запись
#     if not quizzes_database.get(str(message.from_user.id)):
#         quizzes_database[str(message.from_user.id)] = []
#
#     # If user don't have ADMIN permission -
#     if message.poll.type != "quiz":
#         await message.reply("Sorry, only ADMIN")
#         return
#
#     # Сохраняем себе викторину в память
#     quizzes_database[str(message.from_user.id)].append(Quiz(
#         poll_id=message.poll.id,
#         question=message.poll.question,
#         options=[o.text for o in message.poll.options],
#         # if message.poll.type == "quiz":
#         correct_option_id=message.poll.correct_option_id,
#         owner_id=message.from_user.id)
#     )
#     # Сохраняем информацию о её владельце для быстрого поиска в дальнейшем
#     quizzes_owners[message.poll.id] = str(message.from_user.id)
#
#     await message.reply(f'Викторина сохранена. Общее число сохранённых викторин: {len(quizzes_database[str(message.from_user.id)])}')

@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    await message.reply('Contact and location', reply_markup=keyboard2)

# @dp.message_handler(commands=['cancel'])
# async def menu(message: types.Message):
#     remove_keyboard = types.ReplyKeyboardRemove()
#     await message.reply("Menu", reply_markup=remove_keyboard)


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

# @dp.message_handler(state=Form.username)
# async def process_name(message: types.Message, state: FSMContext):
#     """Process user name"""
#     # Finish our conversation
#     username = {message.text}
#     rndFour = sendEmail(gmail_user, username)
#     await state.finish()
#     await message.reply(f"Hello, {message.text}")
#     if code == str(rndFour):
#         await message.reply("/poll")

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

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
