from asyncio import create_task, gather

from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound

from core import dp, bot
from db import AsyncSession
from db.sql import select
from db.base import SubscribeTable

from utils import base
from utils.premium import send_band
from utils.app import send_app
import utils.base as ubase

from module.virtual import VirtualCall
from module.register import RegisterState
from module.premium import bandCall


import template.start as tstart 
import template.virtual as tvirtual
import template.premium as tpremium
import template.payment as tpayment
import template.register as tregister



@dp.message_handler(Text(tstart.VirtualBtn))
async def virtual(ctx : Message, db : AsyncSession):

    user_id = ctx.from_user.id

    request = await db.execute(select(SubscribeTable).where(
        SubscribeTable.user_id == user_id
    ))

    if not (virtual:=request.fetchone()):

        return await ctx.answer(
            text=tvirtual.text,
            reply_markup=tvirtual.kb
        )
    
    virtual : SubscribeTable = virtual[0]

    if not virtual.active:
        
        return await ctx.answer(
            text=tvirtual.text_inactive,
            reply_markup=tvirtual.kb_inactive
        )

    text = tvirtual.text_active.format(
        date=virtual.expire_data
    )

    await ctx.answer(
        text=text,
        reply_markup=tvirtual.kb_active
    )

    await db.close()
        


@dp.callback_query_handler(VirtualCall.filter(action="become"))
async def subcribe(ctx : CallbackQuery, db : AsyncSession):


    await ctx.message.delete()
    # await ctx.message.edit_text(
    #     text=tvirtual.become_text.format(ctx=ctx)
    # )

    markup = await tpayment.pay(
        paid_function="virtual_paid_handler", 
        cancel_function="virtual_cancel_handler"
    )

    await ctx.message.answer(
        text=tvirtual.payment,
        reply_markup=markup
    )

    await db.close()


@dp.callback_query_handler(VirtualCall.filter(action="band"))
async def subcribe(ctx : CallbackQuery, db : AsyncSession):

    await ctx.message.delete()
    await send_band(
        chat_id=ctx.from_user.id, 
        db=db
    )

    await db.close()


@dp.callback_query_handler(VirtualCall.filter(action="app"))
async def main_handler(
    ctx : CallbackQuery,
    db : AsyncSession,
    state : FSMContext,
) -> None:
    """
    Handler of app.
    """

    
    chat_id = ctx.from_user.id

    
    app, data = await gather(
        create_task(base.get_app(db, chat_id)),
        create_task(state.get_data())
    )

    if app is None:
        await ctx.message.delete()

        await ctx.message.answer(
            text=tregister.register_text,
            reply_markup=tregister.register_kb
        )

        return await gather(
            create_task(db.close()),
            create_task(RegisterState.form.set())
        )
    
    app = await send_app(chat_id, app)

    if (app_id:=data.get("app_id")) is not None:
        try:
            await bot.delete_message(chat_id, app_id)
        except MessageToDeleteNotFound:
            ...

    await ctx.message.delete()

    return await gather(
        create_task(db.close()),
        create_task(state.update_data(app_id = app.message_id)),
    )


@dp.callback_query_handler(
    bandCall.filter(),
    state=None
)
async def band_handler(
    query : CallbackQuery,
    callback_data : dict, 
    db : AsyncSession
):
    page = int(callback_data.get('page'))
    act = callback_data.get('action')
    apps = await ubase.get_apps(db)
    user_id = query.from_user.id

    if act == "open":

        await gather(
            create_task(query.message.delete()),
            create_task(send_band(user_id, db, page))
        )            
            
        return await db.close()
    
    elif act == "right":
        kb = tpremium.band_kb(apps, page+1)

    else:
        kb = tpremium.band_kb(apps, page-1)


    return await gather(
        create_task(db.close()),
        create_task(query.message.edit_text(tpremium.band_text, reply_markup=kb))
    )
