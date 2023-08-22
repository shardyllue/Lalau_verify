from aiogram.types import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
)
from db.base import AppTable

from module.moder import PaymentCall
from module.moder import ModerCall
from module.moder import ClubCall, VirtualCall

# import module.moder as mmoder 

club_text = """
Запрос на зачисление в клуб

Пол: {gender}
Полное Имя: {full_name} 
ID Пользователя: {user_id}
Имя Пользователя: @{username},
"""


def club_kb(user_id : int, gender : str):
    return InlineKeyboardMarkup().row(
        InlineKeyboardButton(
            text="✅",
            callback_data=ClubCall.new(
                action="accept",
                user_id=user_id,
                gender=gender
            )
        ),
        InlineKeyboardButton(
            text="❌",
            callback_data=ClubCall.new(
                action="cancel",
                user_id=user_id,
                gender=gender
            )
        )
    )


payment_premium_channel = """
<b>Оплата Premium Канала</b>

Полное имя: {full_name}
ID Пользователя: {user_id}
Имя Пользователя: @{username}
"""


payment_virtual_model = """
<b>Оплата подсписки Virtual Model</b>

Полное имя: {full_name}
ID Пользователя: {user_id}
Имя Пользователя: @{username}
"""


admin_kb = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text="Написать Администратору", url="https://t.me/Chesters_mill")
)



def virtual_kb(user_id : int):
    return InlineKeyboardMarkup().row(
        InlineKeyboardButton(
            text="✅",
            callback_data=VirtualCall.new(
                action="accept",
                user_id=user_id,
            )
        ),
        InlineKeyboardButton(
            text="❌",
            callback_data=VirtualCall.new(
                action="decline",
                user_id=user_id
            )
        )
    )


success_club_women = """
<b>🥳 Поздравляем!</b>

Вы прошли верификацию! Теперь Вы можете вступить в закрытый канал для девушек — черный список спонсоров Lalau.
"""


success_club_men = """
<b>🥳 Поздравляем!</b>

Вы прошли верификацию! Теперь Вы можете вступить в закрытый канал для мужчин - Мужской клуб Lalau.
"""

success_virtual_model = """
<b>🥳 Поздравляем!</b>

Теперь можно перейти к заполнению анкеты... 
"""


cancel_club = """
<b>К сожалению Вы не прошли верификацию!</b>

Обратить к Администратору проекта!
"""

club_link_text = "Вступить в клуб"



kb_accept = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text="✅",
            callback_data="."
        )
    )


kb_decline = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text="❌",
            callback_data="."
        )
    )


app_text = """
Город:  {app.city}
Возраст:  {app.years}
Имя:  {app.name}\n
Рейтинг:  {app.score}
Пользователь:  {app.usrname}\n
Id: {user_id}
"""

app_check_text = "Ваша анкета отправлена на модерацию.\n\nВам придет уведомление, когда модератор подтвердит Вашу анкету"
app_accept_text = "<b>Поздравляем! 🍾</b>\nВаша анкета одобрена!"
app_decline_text = "К сожалению в размещении вашей анкеты отказано. Напишите администратору @chesters_mill"

def app_kb(app : AppTable):
    return InlineKeyboardMarkup().row(
        InlineKeyboardButton(
            text="✅",
            callback_data=ModerCall.new(
                action="accept",
                user_id=app.user_id
            )
        ),
        InlineKeyboardButton(
            text="❌",
            callback_data=ModerCall.new(
                action="decline",
                user_id=app.user_id
            )
        )
    )

    
def raiting_kb(from_id, to_id, page):

    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text="Ввести сумму",
            callback_data=PaymentCall.new(
                action="accept",
                from_id=from_id,
                to_id=to_id,
                page=page
            )
        ),
        InlineKeyboardButton(
            text="Отмена",
            callback_data=PaymentCall.new(
                action="decline",
                from_id=from_id,
                to_id=to_id,
                page=page
            )
        )
    )

    

class Payment:

    text = "Отправьте "

    decline = ""
    accept = ""

    def kb_transfer_close():
        return InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                text="Вы его отменили",
                callback_data="."
            )
        )
    
    def kb_transfer_score(count):
        return InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                text=f"Было зачислено {count} рейтинга",
                callback_data="."
            )
        )
    
    cancel_transferred = "К сожалению в пополнение рейтинга отказано. Напишите администратору @chesters_mill"
    transferred_to = "На Ваш рейтинг зачислено: {score}"
    transferred_from = "Оплата прошла успешно.\n\nСпасибо за покупку"
