from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from module.virtual import VirtualCall

text = """
<b>Этот раздел для тех, кто любит виртуальное общение.</b> 

<i>Мы не несем ответственность за действия наших пользователей! Мы только предоставляем площадку для знакомств</i>
"""

text_inactive = """
<b>Ваша заявка на рассмотрение у Администрации.</b>

<i>Мы пришлем Вам уведомление, когда придет ответ!</i>
"""

text_active = """
<b>Этот раздел для тех, кто любит виртуальное общение.</b> 

<i>Мы не несем ответственность за действия наших пользователей! Мы только предоставляем площадку для знакомств</i>

<b>Ваша подписка актива до {date}</b>
"""

become_text = """
<b>{ctx.from_user.first_name}, чтобы стать Виртуальной моделью надо купить подписку!</b> 
"""

become_models_btn = "Хочу стать вирт моделью"
virtual_app_btn = "Моя анкета"
virtual_models_btn = "⭐️ Анкеты виртуальных моделей"

payment = """
<b>Описание товара</b>

<b>Цена</b>: <i>2000 руб</i>
<b>Тип товара:</b> <i>Статус Virtual Model</i>
<b>Длительность</b>: <i>1 месяц</i>

<b>Время ожидания:</b> <i>около 15 минут</i>
"""


payment_raiting = """
<b>Описание товара</b>

<b>Цена</b>: <i>сумма от 100 до 5000 рублей</i>
<b>Тип товара:</b> <i>Рейтинг</i>
<b>Длительность</b>: <i>1 месяц</i>

<b>Дополнительно:</b>
<i>Рейтинг поднимает Вас в Premium списке. Это значит, что Вас смогут найти больше людей!
Баланс рейтинга ежемесячно обнуляется.</i>

<b>Время ожидания:</b> <i>около 15 минут</i>

"""


paid_text = """
<b>Спасибо за подключение статуса Virtual Model.</b>

<i>Мы Вам пришлем сообщение, когда Администратор рассмотрит Вашу заявку!</i>
"""

paid_raiting = """
<b>Спасибо за приобритение рейтинга</b>

<i>Мы Вам пришлем сообщение, когда Администратор рассмотрит Вашу заявку!</i>
"""


check_raiting = """
<b>Ожидение пополнение рейтига</b>

От: 
- id{from_id} 
- @{username}

Кому:
- id{to_id}
"""


subscribe_expired = """
<b>Подписка <i>"Стаутс Virtual Premium"</i> остановлена!</b> 
"""

kb = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(
        text=become_models_btn,
        callback_data=VirtualCall.new(
            action="become"
        )
    ),
    InlineKeyboardButton(
        text=virtual_models_btn,
        callback_data=VirtualCall.new(
            action="band"
        )
    )
)

kb_inactive = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(
        text=virtual_models_btn,
        callback_data=VirtualCall.new(
            action="band"
        )
    )
)

kb_active = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(
        text=virtual_app_btn,
        callback_data=VirtualCall.new(
            action="app"
        )
    ),
    InlineKeyboardButton(
        text=virtual_models_btn,
        callback_data=VirtualCall.new(
            action="band"
        )
    )
)

kb_app = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(
        text=virtual_app_btn,
        callback_data=VirtualCall.new(
            action="app"
        )
    )
)
