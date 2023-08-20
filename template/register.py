from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import template.base as tbase
import static


register_text = """
<b>Походу Мы не нашли анкету на Ваше имя.</b>\n\nХотите создать анкету?
"""

register_btn_yes = "✅ Да, хочу создать анкету"

register_kb = ReplyKeyboardMarkup(
    one_time_keyboard=True,
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(register_btn_yes)],
        [KeyboardButton(tbase.back_text)]
    ]
)



gender_text = """
<b>Вы мужчина или девушка?</b>"
"""

gender_male_btn = "Мужчина"
gender_female_btn = "Девушка"    

gender_kb = ReplyKeyboardMarkup(
    one_time_keyboard=True,
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text=gender_male_btn), 
            KeyboardButton(text=gender_female_btn)
        ],
        [KeyboardButton(text=tbase.back_text)]
    ]
)


back_kb = ReplyKeyboardMarkup(
    one_time_keyboard=True,
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text=tbase.back_text)]
    ]
)





name = "<b>Как Вас зовут?</b>"
err_name = "⚠️<b>Невалидное имя!</b>\n\n<i>• Используйте только буквы Русского/Английского языка.\n• Имя не может быть длинее 15 символов.</i>"

years = "<b>{name}, cколько Вам лет?</b>"
err_years = "⚠️<b>Невалидный возраст!</b>\n\n<i>• Используйте только цифры.\n• Вам должно быть 18 лет или больше.</i>"

city = "<b>Из какого Вы города?</b>"
err_city = "⚠️<b>Невалидный город!</b>\n\n<i>• Используйте только буквы Русского/Английского языка.\n• Город не может быть длинее 20 символов.</i>"



usr_photo = static.usrname

usr_text = """
<b>Теперь определимся с именем пользователя</b>\n\nПример: @lalau
"""

usr_err = """
⚠️<b>Невалидное имя пользователя!</b>.\n\n<i>• Имя должно начинаться c «@».</i>\n<i>• Имя должно быть от 5 символов.</i>
"""

usr_err_tg = """
⚠️<b>Невалидное имя пользователя!</b>\n\n<i>• Имя пользователя должно быть установлено.</i>
"""

usr_username_btn = "Взять с моего аккаунта"

usr_kb = ReplyKeyboardMarkup(
    one_time_keyboard=True,
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text=usr_username_btn)],
        [KeyboardButton(text=tbase.back_text)]
    ]
)

photo_text = """
<b>Отлично! Отправьте свою фотографию</b>\n\n<i>⚠️Ваша фотография будет видна всем</i>!
"""



photo_err = "Отправьте фотографию!"


photo_kb = ReplyKeyboardMarkup(
    one_time_keyboard=True,
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text=tbase.back_text)]
    ]
)


video_text = """
<b>Теперь Вам нужно записать видеосообщение («видео в кружочке»)</b>
"""


video_err = "Отправьте видео!"


video_kb = ReplyKeyboardMarkup(
    one_time_keyboard=True,
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text=tbase.back_text)]
    ]
)

pub_video_text = """
<b>Разрешаете ли показывать Ваше видеосообщение («видео в кружочке») участникам премиум канала?</b>
"""

pub_video_accept_btn = "✅ Да, Я разрешаю!"
pub_video_dicline_btn = "*️⃣ Нет!"

pub_video_kb = ReplyKeyboardMarkup(
    one_time_keyboard=True,
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text=pub_video_accept_btn), KeyboardButton(pub_video_dicline_btn)],
        [KeyboardButton(text=tbase.back_text)]
    ]
)

success = """
✅ Проверьте анкету и отправьте на модерацию администратору!
"""