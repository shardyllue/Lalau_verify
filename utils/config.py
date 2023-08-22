from dotenv import load_dotenv
from os import environ

load_dotenv()

TOKEN = environ.get("TOKEN")

PG_URL = environ.get("PG_URL")

MODER_GROUP = int(environ.get("MODER_GROUP_ID"))
STORAGE_GROUP = int(environ.get("STORAGE_GROUP_ID"))
PUBLIC_GROUP = int(environ.get("PUBLIC_GROUP_ID"))


ALLOW_SYMBOL_RU = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя-_@ 1234567890"
ALLOW_SYMBOL_EN = "abcdefghijklmnopqrstuvwxyz-_@ 1234567890"


LINK_CLUB_WOMEN = "https://t.me/+ZebXp367A3VhNzhi"
LINK_CLUB_MEN = "https://t.me/+IHMm8J64jZQ1ODEy"


MUTE_WORD = [
    "вирт", "видео"
]

