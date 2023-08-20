from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


from module.edit import EditCall
from module.app import UserCall

import template.base as tbase



def title(text : str):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(
            text=text, 
            callback_data="."
        ),
        InlineKeyboardButton(
            text=tbase.back_text, 
            callback_data=EditCall.new(
                value="cancel"
            )
        )
    )



kb =  InlineKeyboardMarkup().add(
    InlineKeyboardButton(
    text="📝 Редактировние",
    callback_data=EditCall.new(
        value="."
    )
)
).row(
InlineKeyboardButton(
    text="Имя",
    callback_data=EditCall.new(
        value="name"
    )
),
InlineKeyboardButton(
    text="Возраст",
    callback_data=EditCall.new(
        value="years"
    )
),
).row(
InlineKeyboardButton(
    text="Город",
    callback_data=EditCall.new(
        value="city"
    )
),
InlineKeyboardButton(
    text="@Имя",
    callback_data=EditCall.new(
        value="usrname"
    )
)
).row(
InlineKeyboardButton(
    text="Фото",
    callback_data=EditCall.new(
        value="photo"
    )
),       
InlineKeyboardButton(
    text="Видео",
    callback_data=EditCall.new(
        value="video"
    )
)
).add(        
InlineKeyboardButton(
    text=tbase.back_text,
    callback_data=UserCall.new(
        action="open.control"
    )
)
)


edit_title_name = "Отправьте новое имя"
edit_title_years = "Отправьте возраст"
edit_title_city = "Отправьте новый город"
edit_title_usrname = "Отправьте новое @имя"
edit_title_photo = "Отправьте новое фото"
edit_title_video = "Отпрвьте новое видео"