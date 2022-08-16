from flask import Flask
import logging
from aiogram import Bot, Dispatcher, executor, types

TOKEN_API = '639642745:AAHd9aIHomuZZH7-pxJPRpWAAdMjF4vHRWc'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot)

app = Flask(__name__)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")

@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
