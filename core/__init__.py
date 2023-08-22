from os import path

from aiogram import Dispatcher, Bot
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.files import JSONStorage

from utils.config import TOKEN
from utils.mute import MuteStorage

storage = JSONStorage(path.join("data/storage.json"))

mute_storage = MuteStorage(path.join("data/mute.json"))

bot = Bot(
    token=TOKEN,
    parse_mode=ParseMode.HTML,
)
dp = Dispatcher(
    bot=bot,
    storage=storage,
)

