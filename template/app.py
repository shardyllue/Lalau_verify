from json import dumps

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.deep_linking import get_start_link

from db.base import AppTable

from module.edit import EditCall
from module.premium import appCall, bandCall 
from module.app import UserCall as AppUserCall
from module.payment import UserCall as PayUserCall

import template.base as Tbase



app_text = """
Город:  {app.city}
Возраст:  {app.years}
Имя:  {app.name}

Рейтинг:  {app.score}
Пользователь:  {app.usrname}
"""

app_delete = """<b>Вы удалили анкету</b>\n\n<i>В любой момент Вы сможете создать её занова!</i>"""


def app_kb(app : AppTable):

    _kb = InlineKeyboardMarkup(row_width=1)


    if app.video_id is not None:
        _kb.add(
            InlineKeyboardButton(
                text="👁 Моё видео",
                callback_data=AppUserCall.new(
                    action="open.video"
                )
            ),    
            InlineKeyboardButton(
                text=(
                    "🟢 Статус видео: Публичный" 
                    if app.pub_video else 
                    "*️⃣ Статус видео: Приватный"),
                callback_data=(
                    EditCall.new(value="switch.video.off") 
                    if app.pub_video else 
                    EditCall.new(value="switch.video.on") 
                )
            ),
            InlineKeyboardButton(
                text=(
                    "🟢 Показывать в общей группе: Да" 
                    if app.post_app else 
                    "*️⃣ Показывать в общей группе: Нет"),
                callback_data=(
                    EditCall.new(value="switch.channel.off") 
                    if app.post_app else 
                    EditCall.new(value="switch.channel.on") 
                )
            )
        )

    _kb.add(
        InlineKeyboardButton(
            text="📝 Редактировать",
            callback_data=AppUserCall.new(
                action="open.edit"
            )
        )
    ).row(
        InlineKeyboardButton(
            text="❌ Удалить",
            callback_data=AppUserCall.new(
                action="delete"
            )
        ),InlineKeyboardButton(
            text="🔝 Рейтинг",
            callback_data=AppUserCall.new(
                action="pay_raiting",
            )
        ),        
    )


    if app.moderated is False:
        _kb.add(
            InlineKeyboardButton(
                text="⏺ На модерации ...",
                callback_data="."
            )
        )

    elif app.moderated is None:
        _kb.add(
            InlineKeyboardButton(
                text="Анкета отклонена",
                callback_data="."
            )
        )   

    return _kb    

    
premium_text = """
Город:  {app.city}
Возраст:  {app.years}
Имя:  {app.name}\n
Пол:  {app.gender}
Рейтинг:  {app.score}
Пользователь:  {app.usrname}
"""


premium_err = """
📎 Походу пользователь решил удалить свою анкету или изменить её, подождите пока пользователю одобрять анкету или он её создать!
"""


premium_getting = """🔍 Подождите... ищем анкету пользователя"""


def premium_kb(
    app : AppTable, 
    chat_id : int,
    photo_mode : bool = True, 
    page : int = 0
):
    _kb = InlineKeyboardMarkup()


    if (app.video_id is not None) and (app.pub_video is True):

        if photo_mode:
            _kb.add(
                InlineKeyboardButton(
                    text="📸 Видео", 
                    callback_data=appCall.new(
                        action="video", 
                        user_id=app.user_id, 
                        page=page
                    )
                ),
            )
        else:
            _kb.add(
                InlineKeyboardButton(
                    text="📸 фото", 
                    callback_data=appCall.new(
                        action="open", 
                        user_id=app.user_id, 
                        page=page
                    )
                ),
            )

    _kb.row(
        InlineKeyboardButton(
            text="🎁 Чаевые", 
            callback_data=PayUserCall.new(
                action="form",
                from_id=chat_id,
                to_id=app.user_id,
                page=page
            )
        ),
        InlineKeyboardButton(
            text=Tbase.back_text,
            callback_data=bandCall.new(action="open", page=page)
        ),
    )

    return _kb


    
posting_text = """
<b>Виртуальное общение</b>

Город:  {app.city}
Возраст:  {app.years}
Имя:  {app.name}

Рейтинг:  {app.score}
"""


async def posting_kb(username : str, user_id : int, page = int):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text="Перейти в профиль",
            url=await get_start_link(
                payload=dumps({
                    "user_id" : user_id,
                    "page" : page
                }),
                encode=True
            )
        )
    )


video_text = "Видео отправлено ниже"
video_btn_skip = "Убрать"


video_kb = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        text=video_btn_skip,
        callback_data=AppUserCall.new(
            action="close.video"
        )
    )
)