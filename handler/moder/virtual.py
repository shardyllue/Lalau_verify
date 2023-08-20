import datetime as dt

from aiogram.types import CallbackQuery, ChatPermissions
from core import dp, bot


from db import AsyncSession
from db.sql import update, delete
from db.base import SubscribeTable, AppTable

from loguru import logger

import module.moder as mmoder 
import template.moder as tmoder
import template.virtual as tvirtual



@dp.callback_query_handler(
    mmoder.VirtualCall.filter(action="accept")
)
async def club_moder_handler(
    ctx : CallbackQuery,
    callback_data : dict,
    db : AsyncSession
):
    user_id = int(callback_data.get("user_id"))
    

    await ctx.message.edit_reply_markup(
        reply_markup=tmoder.kb_accept
    )
    
    await bot.send_message(
        chat_id=user_id,
        text=tmoder.success_virtual_model,
        reply_markup=tvirtual.kb_app
    )

    await db.execute(
        update(AppTable).where(
            AppTable.user_id == user_id
        ).values(moderated = True)
    )

    try:
        user_state = dp.current_state(user=user_id, chat=user_id)

        user_data = await user_state.get_data()
        
        app_id = user_data.get("app_id")

        await bot.delete_message(user_id, app_id)
    except Exception as exp:
        logger.warning(exp)


    await db.execute(update(SubscribeTable).where(
        SubscribeTable.user_id == user_id
    ).values(active = True, expire_data=dt.datetime.now() + dt.timedelta(days=30)))


    await db.commit()

    # await bot.restrict_chat_member(
    #     chat_id="", 
    #     user_id=user_id,
    #     permissions=ChatPermissions(True))


@dp.callback_query_handler(
    mmoder.VirtualCall.filter(action="decline")
)
async def club_moder_handler(
    ctx : CallbackQuery,
    callback_data : dict,
    db : AsyncSession
):

    user_id = int(callback_data.get("user_id"))

    await ctx.message.edit_reply_markup(
        reply_markup=tmoder.kb_decline
    )

    await db.execute(
        delete(SubscribeTable).where(
            SubscribeTable.user_id == user_id
        )
    )

    try:
        user_state = dp.current_state(user=user_id, chat=user_id)

        user_data = await user_state.get_data()
        
        app_id = user_data.get("app_id")

        await bot.delete_message(user_id, app_id)
    except Exception as exp:
        logger.error(exp)
    

    await bot.send_message(
        chat_id=user_id,
        text=tmoder.cancel_club,
        reply_markup=tmoder.admin_kb
    )


    await db.commit()