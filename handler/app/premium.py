from asyncio import gather, create_task

from core import dp, bot

from aiogram import types
from aiogram.dispatcher import FSMContext

from db import AsyncSession
from db.base import AppTable
from db.sql import delete 

from module.payment import UserCall

from utils.premium import send_video_premium, send_app_premium

import utils.base as Ubase

import template.app as tapp
import module.premium as Mpremium
import template.payment as tpayment
import template.virtual as tvirtual


@dp.callback_query_handler(
    Mpremium.appCall.filter(action="open"),
    state=None
)
async def open_handler(
    query : types.CallbackQuery, 
    callback_data : dict,
    db : AsyncSession,
):
    """
    open app handler
    """

    app_user_id = int(callback_data["user_id"])
    page = int(callback_data["page"])
    user_id = query.from_user.id
    app = await Ubase.get_app(db, app_user_id)

    if not app:
        return await gather(
            create_task(query.answer(tapp.premium_err)),
            create_task(db.close())
        )

    return await gather(
        create_task(query.message.delete()),
        create_task(send_app_premium(user_id, app, page)),
        create_task(db.close()),
    )


@dp.callback_query_handler(
    Mpremium.appCall.filter(action="video"),
    state=None
)
async def video_handler(
    query : types.CallbackQuery, 
    callback_data : dict,
    db : AsyncSession,
):
    """
    Video handler
    """
    app_user_id = int(callback_data["user_id"])
    page = int(callback_data["page"])
    user_id = query.from_user.id

    app = await Ubase.get_app(db, app_user_id)

    if not app:
        return await gather(
            create_task(query.answer(tapp.premium_err)),
            create_task(db.close()),
        )

    return await gather(
        create_task(query.message.delete()),
        create_task(send_video_premium(user_id, app,page)),
        create_task(db.close()),
    )



@dp.callback_query_handler(
    UserCall.filter(action="form")
)
async def ggg_handler(
    ctx : types.CallbackQuery,
    callback_data : dict,
    state : FSMContext
):
    await ctx.message.delete()

    data = {
        "from_id" : callback_data.get("from_id"),
        "to_id" : callback_data.get("to_id"),
        "page" : callback_data.get("page")
    }

    markup = await tpayment.pay(
        paid_function="virtual_paid_raiting", 
        cancel_function="virtual_cancel_raiting",
        state = state,
        data = data
    )

    await ctx.message.answer(
        text=tvirtual.payment_raiting,
        reply_markup=markup
    )    