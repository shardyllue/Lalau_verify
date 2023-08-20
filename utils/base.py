from typing import List
from json import dumps, loads

from asyncio import sleep
from core import bot

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from db import AsyncSession
from db.sql import select
from db.base import AppTable, SubscribeTable

from utils.config import STORAGE_GROUP


def callback_dumps(obj):

    json = dumps(obj)

    return json.replace(":", "$%$")


def callback_loads(obj : str):

    json_string = obj.replace("$%", ":")

    return loads(json_string)


def link_kb(text : str, link : str):

    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text=text, 
            url=link
        )
    )


def splite_array(
    array : list, chunk : int
) -> list:
    """
    
    split a python list in half.
    
    """
    count_chunks = len(array)//chunk
    new_list = []

    for i in range(0, count_chunks + 1):

        start_with = 0 + chunk*i
        finish_with = chunk + chunk*i


        new_list.append(
            array[start_with:finish_with]
        )


    return new_list

    
async def get_app(
    db : AsyncSession,
    user_id : int, 
) -> AppTable | None:
    """
    
    Get app from db
    
    """
    request = await db.execute(
        select(AppTable).where(
            AppTable.user_id == user_id
        )
    )

    if (app:=request.fetchone()) is None:
        return None
    
    return app[0]


async def get_apps(db : AsyncSession, public = False) -> List[AppTable]:
    """
    
    Get apps from db
    
    """

    
    request_subs = await db.execute(
        select(SubscribeTable.user_id).where(
            SubscribeTable.active == True
        )
    )

    if not public:
        request_app = await db.execute(
            select(AppTable).where(
                AppTable.moderated == True
            ).order_by(AppTable.score)
        )

    else:
        request_app = await db.execute(
            select(AppTable).where(
                (AppTable.photo_id != None),
                (AppTable.moderated == True),
                (AppTable.post_app == True)
            )
        )

    data_apps = request_app.fetchall()[::-1]
    data_subs = request_subs.fetchall()
    
    apps = [app[0] for app in data_apps]  
    subs = [sub[0] for sub in data_subs]

    result = []

    for app in apps:

        app_id = app.user_id

        for sub in subs:

            if app_id != sub:
                continue
            
            result.append(app)


    return result


async def delay(
    ctx : types.Message,
    time : int = 5
) -> None:
    """
    
    send a delaied message

    """

    message = await ctx

    await sleep(time)

    return await message.delete()


async def get_save_photo_id(ctx : types.Message) -> int:
    """
    
    get video_id from the storage group

    """
    data = await bot.send_photo(
        photo=ctx.photo[0].file_id,
        chat_id=STORAGE_GROUP
    )

    return data.photo[0].file_id


async def get_save_video_id(ctx : types.Message) -> int:
    """
    
    get photo_id from the storage group

    """


    data = await bot.send_video_note(
        video_note=ctx.video_note.file_id,
        chat_id=STORAGE_GROUP
    )

    return data.video_note.file_id