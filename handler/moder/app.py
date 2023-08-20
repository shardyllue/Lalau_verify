from core import dp, bot
from asyncio import gather, create_task

from loguru import logger

from utils import config

from aiogram import types
from aiogram.dispatcher import filters
from aiogram.dispatcher import FSMContext

from db import AsyncSession
from db.sql import update
from db.base import AppTable

import utils.base as Ubase
import template.start as tstart
import template.moder as tmoder
import module.moder as Mmoder
import static


# @dp.callback_query_handler(
#     Mmoder.ModerCall.filter(action="post.moderate"),
#     state=None,
# )
# async def moderate_handler(
#     query : types.CallbackQuery,
#     callback_data : dict,
#     state : FSMContext,
#     db : AsyncSession,
# ):
#     """
#     Premium.
#     """
#     user_id = query.from_user.id
#     app = await Ubase.get_app(db, user_id)

#     tasks = []

#     if app.video_id:
#         tasks.append(bot.send_video_note(
#             chat_id=config.MODER_GROUP,
#             video_note=app.video_id
#         ))

#     tasks.append(db.execute(update(AppTable).where(
#         AppTable.user_id == user_id).values(moderated = None)))

#     await gather(*tasks)

#     caption = tmoder.app_text.format(app=app, query=query)


#     return await gather(
#         create_task(db.commit()),
#         create_task(query.message.delete()),
#         create_task(query.message.answer(tmoder.app_check_text, reply_markup=tstart.kb)),
#         create_task(bot.send_photo(
#             chat_id=config.MODER_GROUP,
#             photo=app.photo_id,
#             caption=caption,
#             reply_markup=tmoder.app_kb(app)
#         ))
#     )
    

@dp.callback_query_handler(
    Mmoder.ModerCall.filter(action="accept"),
    state="*"
)
async def accept_handler(
    query : types.CallbackQuery,
    callback_data : dict,
    state : FSMContext,
    db : AsyncSession,
):
    """
    Accept handler
    """
    user_id = int(callback_data["user_id"])

    await db.execute(
        update(AppTable).where(
            AppTable.user_id == user_id
        ).values(moderated = True)
    )

    try:
        user_state = dp.current_state(user=user_id, chat=user_id)

        user_data = await user_state.get_data()
        
        await bot.delete_message(user_id, user_data.get("app_id"))
    except Exception as exp:
        logger.error(exp)

    send_usr = bot.send_message(user_id, tmoder.app_accept_text)
    update_moder = query.message.edit_reply_markup(
        reply_markup=tmoder.kb_accept
    )

    return await gather(
        create_task(update_moder),
        create_task(send_usr),
        create_task(db.commit())
    )



@dp.callback_query_handler(
    Mmoder.ModerCall.filter(action="decline"),
    state="*"
)
async def decline_handler(
    query : types.CallbackQuery,
    callback_data : dict,
    state : FSMContext,
    db : AsyncSession,
):
    """
    Decline handler
    """
    user_id = int(callback_data["user_id"])

    await db.execute(
        update(AppTable).where(
            AppTable.user_id == user_id
        ).values(moderated = False)
    )

    try:
        user_state = dp.current_state(user=user_id, chat=user_id)

        user_data = await user_state.get_data()
        
        await bot.delete_message(user_id, user_data.get("app_id"))
    except Exception as exp:
        logger.error(exp)

    send_usr = bot.send_message(user_id, tmoder.app_decline_text)
    update_moder = query.message.edit_reply_markup(
        reply_markup=tmoder.kb_decline
    )

    return await gather(
        create_task(db.commit()),
        create_task(update_moder),
        create_task(send_usr),
    )















