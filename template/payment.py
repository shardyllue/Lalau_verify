from typing import Callable

from aiogram.types import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from aiogram.dispatcher import FSMContext

from module.payment import PaymentCall
# import module.premium as Mpremium
# import module.payment as mpayemnt

import template.base as tbase




async def pay(
    paid_function : str, 
    cancel_function : str,
    state : FSMContext = None,
    data : dict = None   
):

    if state:
        await state.set_data(data)

    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(
            text="💳 Карта",
            callback_data=PaymentCall.new(
                action="pay",
                paid_function=paid_function,
                cancel_function=cancel_function
            ),
        ),
        InlineKeyboardButton(
            text=tbase.back_text,
            callback_data=PaymentCall.new(
                action="cancel",
                paid_function=paid_function,
                cancel_function=cancel_function
            ),
        )
    )   


payment_data = """
`6764 5444 4360 9839` - Сбербанк
`W1SEFOX` - Qiwi
*Тыкни на номер, он автоматически скопируется!*

Отправьте боту квитанцию об оплате.

На квитанции должны быть четко видны: *дата*, *время* и *сумма платежа*!
"""

premium_payment_data = """
`6764 5444 4360 9839` - Газпромбанк 

*Тыкни на номер, он автоматически скопируется!*

Отправьте боту квитанцию об оплате.

На квитанции должны быть четко видны: *дата*, *время* и *сумма платежа*!
"""

payment_channel = """
<b>Свяжитесь с Администратором канала для получения доступа</b>
"""


payment_btn_cancel = tbase.back_text


kb_cancel = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text=payment_btn_cancel)]
    ]
)

