import os
import re
import traceback
import time
import requests
import configparser
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import BoundFilter
import db

config = configparser.ConfigParser()
config.read("settings.ini")
TOKEN = config["tgbot"]["token"]
admin_id = int(config["tgbot"]["admin_id"])

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class Info(StatesGroup):
    adminka = State()
    rassilka = State()

if not os.path.exists('audio'):
	os.makedirs('audio')

def get_download_links(video_url):
    r = requests.get(f'https://api.douyin.wtf/api?url={video_url}').json()
    if r["status"] == "success":
        video_url = r["nwm_video_url"]
        video_r = requests.get(video_url).content
        return video_r
    return None

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
	if db.get_users_exist(message.chat.id) == False:
		db.add_user_to_db(message.chat.id)
		if message.chat.id == admin_id:
			await bot.send_message(chat_id=message.chat.id, text='📼 Привет, я помогу тебе скачать видео с TikTok.')
		else:
			await bot.send_message(chat_id=message.chat.id, text='📼 Привет, я помогу тебе скачать видео с TikTok.')
	else:
		if message.chat.id == admin_id:
			await bot.send_message(chat_id=message.chat.id, text='📼 Привет, я помогу тебе скачать видео с TikTok.')
		else:
			await bot.send_message(chat_id=message.chat.id, text='📼 Привет, я помогу тебе скачать видео с TikTok.')

@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    if message.text.startswith(('https://www.tiktok.com','http://www.tiktok.com', 'https://vm.tiktok.com', 'http://vm.tiktok.com')):
        video_url = message.text
        video_r = get_download_links(video_url)
        if video_r != None:
            await bot.send_video(chat_id=message.chat.id, video=video_r)
        else:
            await bot.send_message(chat_id=message.chat.id, text='Ошибка при скачивании.')
    else:
        await bot.send_message(chat_id=message.chat.id, text='Я тебя не понял.')
if __name__ == "__main__":
	db.check_db()
	executor.start_polling(dp, skip_updates=True)
