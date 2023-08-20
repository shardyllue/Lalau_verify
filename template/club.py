from os import path

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



_images_woman_path = path.join("template", "image", "woman.png")
_images_man_path = path.join("template", "image", "man.png")


def women_image():
    return open(_images_woman_path, "rb")


def men_image():
    return open(_images_man_path, "rb")



women_text = """
<b>👩 Пришлите видеосообщение «кружок» с жестом как на примере</b>

<i>Кружок должен быть сделать при достаточном освещении.</i>
"""


men_text = """
<b>👨 Пришлите видеосообщение «кружок» с жестом как на примере</b>

<i>Кружок должен быть сделать при достаточном освещении.</i>
"""


cancel = "🔙 Назад"


kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text=cancel)]
    ]    
)


moder = """
<b>⏱️ Ваша верификация будет проверена в среднем в течении 15 минут.</b>
<i>В ночное время может потребоваться больше времени.</i>

<b>🔔 Мы пришлем уведомление как будет готово, ожидайте пожалуйста!</b> 
"""
