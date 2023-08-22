from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from db.base import AppTable

from module.premium import appCall, bandCall, premiumCall


channel_text = """
<b>Premium🏆 канал</b> — отличается от основного канала допуском в него только реальных, красивых, ярких девушек, которые ищут себе успешного мужчину.
Для девушек вход бесплатный, но действуют критерии отбора по внешности и проверка на реальность.
Для мужчин доступ в канал платный, стоимость 3000 рублей.
"""

channel_btn_man = "Мужчина"
channel_btn_womam = "Девушка"

channel_kb = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        text=channel_btn_man,
        callback_data=premiumCall.new(
            action=channel_btn_man
        )
    ),
    InlineKeyboardButton(
        text=channel_btn_womam,
        callback_data=premiumCall.new(
            action=channel_btn_womam
        )
    )
)

channel_link_admin = "t.me/Chesters_mill"
channel_link_womam_text = "Написать Администратору"
channel_link_man_text = "Написать Администратору"
channel_response_woman = """
{ctx.from_user.first_name}, чтобы попасть в Premium Канал надо пройти верификацию!

<b>Для прохождения верификации необходимо связаться с Администратором проекта Lalau</b>
"""


channel_response_man_1 = """
{ctx.from_user.first_name}, чтобы попасть в Premium Канал надо оплатить вход!
"""
channel_response_man_2 = """
<b>Описание товара</b>

<b>Цена</b>: <i>3000 руб</i>
<b>Тип товара:</b> <i>Доступ к премиум каналу</i>

<b>Время ожидания:</b> <i>около 15 минут</i>
"""

channel_response_man_3 = """
<b>Свяжитесь с Администратором для получения доступа.</b>
"""

payment_success = """
<b>Спасибо за оплату услуги</b> <i>Premium Канал</i>!
"""


band_text = """
Уважаемые подписчики премиум-канала "lalau", для удобства знакомства с другими участниками мы создали список анкет участников проекта, которые ищут знакомства.
Напоминаем, что "lalau" категорически против услуг проституции, порнографии и всему, что запрещено Уголовным кодексом Российской Федерации.
"""

band_leader_icon = {0 : "🥇", 1 : "🥈", 2 : "🥉"}

def band_kb(
    apps : List[AppTable],
    page : int = 0,
):
    _kb = InlineKeyboardMarkup()

    pages = apps.__len__() // 9
    start_with = 0 + 9*page
    finish_with = 9 + 9*page

    
    
    for index, app in enumerate(apps[start_with:finish_with]):
        if (index in range(0, 3)) and (page == 0):
            front = f"{band_leader_icon[index]}"
            back = ""
        else:
            front = ""
            back = f", Рейтинг: {app.score}"

        _kb.add(
            InlineKeyboardButton(
                text=f"{front}{app.city}, {app.name}, {app.years} лет{back}", 
                callback_data=appCall.new(action="open", user_id=app.user_id, page=page)
            ),
        )
    

    return _kb.row(
        InlineKeyboardButton(
            text="⬅️" if page > 0 else " ", 
            callback_data=bandCall.new(
                action="left", page=page
            ) if page > 0 else " "
        ),
        InlineKeyboardButton(
            text=f"{page + 1} / {pages + 1}", 
            callback_data="."
        ),
        InlineKeyboardButton(
            text="➡️" if page < pages else " ", 
            callback_data=bandCall.new(
                action="right", page=page
            ) if page < pages else " "
        ),
    )

    
