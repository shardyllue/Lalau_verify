from asyncio import gather, create_task
from utils import config

from core import bot

from db import AsyncSession
from db.sql import update
from db.base import AppTable


import utils.base as ubase
import template.moder as tmoder
import static


async def moderate(
    user : int | AppTable,
    db : AsyncSession,
):
    """
    Premium.
    """

    if not isinstance(user, AppTable):
        app = await ubase.get_app(db, user)
        user_id = user

        sql = update(AppTable).where(
            AppTable.user_id == user_id
        ).values(moderated = None)

        await db.execute(sql)
    else:
        app = user
        user_id = user.user_id


    if app.video_id:
        await bot.send_video_note(
            chat_id=config.MODER_GROUP,
            video_note=app.video_id
        )

    if not app.photo_id:
        photo_id = static.anon
    else:
        photo_id = app.photo_id


    await bot.send_photo(
        chat_id=config.MODER_GROUP,
        photo=photo_id,
        caption=tmoder.app_text.format(app=app,user_id=app.user_id),
        reply_markup=tmoder.app_kb(app)
    )