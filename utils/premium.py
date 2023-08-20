from db import AsyncSession
from db.base import AppTable

from core import bot

from utils import config
from utils.base import get_apps

import template.app as tapp
import template.premium as tpremium
import static




async def send_band(
    chat_id : int, 
    db : AsyncSession, 
    page : int = 0
):
    apps = await get_apps(db)
    kb = tpremium.band_kb(apps, page)

    return await bot.send_message(
        chat_id=chat_id,
        text=tpremium.band_text,
        reply_markup=kb
    )


async def send_app_premium(
    chat_id  : int, app : AppTable, page : int = 0
):

    kb = tapp.premium_kb(app=app, chat_id=chat_id, page=page)
    caption = tapp.premium_text.format(app=app)


    return await bot.send_photo(
        chat_id=chat_id,
        caption=caption,
        photo=app.photo_id if app.photo_id else static.anon,
        reply_markup=kb
    )


async def send_app_premium_group(app : AppTable, page : int = 0):

    me = await bot.get_me()

    kb = await tapp.posting_kb(
        username=me.username,
        user_id=app.user_id,
        page=page
    )


    caption = tapp.posting_text.format(app=app)

    return await bot.send_photo(
        chat_id=config.PUBLIC_GROUP,
        caption=caption,
        photo=app.photo_id,
        reply_markup=kb
    )


async def send_video_premium(
    chat_id : int, app : AppTable, page : int = 0
):
    return await bot.send_video_note(
        chat_id=chat_id,
        video_note=app.video_id,
        reply_markup=tapp.premium_kb(
            app=app, 
            chat_id=chat_id, 
            page=page, 
            photo_mode=False
        )
    )
