from aiogram.types import CallbackQuery, ChatPermissions
# from aiogram.types import CallbackQuery, ChatPermissions
from core import dp, bot
from db import AsyncSession

from utils import config

import utils.base as ubase
import module.moder as mmoder 
import template.moder as tmoder



@dp.callback_query_handler(
    mmoder.ClubCall.filter(action="accept")
)
async def club_moder_handler(
    ctx : CallbackQuery,
    callback_data : dict,
    db : AsyncSession
):
    gender = callback_data.get("gender")
    user_id = callback_data.get("user_id")
    

    await ctx.message.edit_reply_markup(
        reply_markup=tmoder.kb_accept
    )
    
    if gender == "Мужчина":

        form_text = tmoder.success_club_men
        link = config.LINK_CLUB_MEN
    
    else:

        form_text = tmoder.success_club_women
        link = config.LINK_CLUB_WOMEN
    

    await bot.send_message(
        chat_id=user_id,
        text=form_text,
        reply_markup=ubase.link_kb(
            text=tmoder.club_link_text,
            link=link
        )
    )

    await db.close()

    # await bot.restrict_chat_member(
    #     chat_id="", 
    #     user_id=user_id,
    #     permissions=ChatPermissions(True))


@dp.callback_query_handler(
    mmoder.ClubCall.filter(action="cancel")
)
async def club_moder_handler(
    ctx : CallbackQuery,
    callback_data : dict,
    db : AsyncSession
):

    user_id = callback_data.get("user_id")

    await ctx.message.edit_reply_markup(
        reply_markup=tmoder.kb_decline
    )
    

    await bot.send_message(
        chat_id=user_id,
        text=tmoder.cancel_club,
        reply_markup=tmoder.admin_kb
    )

    await db.close()
