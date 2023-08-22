import datetime as dt
from asyncio import gather, create_task

from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound
from aiogram.types import CallbackQuery, Message, ContentTypes

from core import dp, bot
from utils import config

from db import AsyncSession
from db.base import SubscribeTable

from module.register import RegisterState

import module.payment as mpayemnt

import utils.base as ubase
import utils.premium as Upremium
from utils.app import send_app
import utils.base as ubase

import template.base as Tbase
import template.payment as tpayment
import template.premium as tpremium
import template.start as tstart
import template.moder as tmoder
import template.virtual as tvirtual
import template.register as tregister







async def premium_paid_channel(
    ctx : Message, 
    state : FSMContext, 
    db : AsyncSession
):

    await ctx.answer(
        text=tpremium.payment_success,
        reply_markup=tstart.kb
    )

    await ctx.answer(
        text=tpremium.channel_response_man_3,
        reply_markup=ubase.link_kb(
            text=tpremium.channel_link_man_text,
            link=tpremium.channel_link_admin
        )
    )

    first_name = ctx.from_user.first_name
    last_name = ctx.from_user.last_name
    user_id = ctx.from_user.id
    username = ctx.from_user.username

    if not last_name:
        full_name = first_name

    else:
        full_name = first_name + " " + last_name
        
    
    
    text = tmoder.payment_premium_channel.format(
        full_name = full_name,
        user_id = user_id,
        username = username
    )

    await bot.send_photo(
        chat_id=config.MODER_GROUP,
        photo=ctx.photo[-1].file_id,
        caption=text
    )


    await state.set_state(None)
    await db.close()


async def premium_cancel_channel(
    ctx : Message, 
    state : FSMContext, 
    db : AsyncSession
):

    await bot.send_message(
        chat_id=ctx.from_user.id,
        text=tstart.text,
        reply_markup=tstart.kb
    )


    await state.set_state(None)
    await db.close()




async def virtual_paid_handler(
    ctx : Message, 
    state : FSMContext, 
    db : AsyncSession
):
    """
    
    Virtual paid

    """
    
    await ctx.answer(
        text=tvirtual.paid_text,
        reply_markup=tstart.kb
    )

    first_name = ctx.from_user.first_name
    last_name = ctx.from_user.last_name
    user_id = ctx.from_user.id
    username = ctx.from_user.username
    expire_date = dt.datetime.now() + dt.timedelta(days=30)

    if not last_name:
        full_name = first_name

    else:
        full_name = first_name + " " + last_name


    text = tmoder.payment_virtual_model.format(
        full_name = full_name,
        user_id = user_id,
        username = username
    )

    await bot.send_photo(
        chat_id=config.MODER_GROUP,
        photo=ctx.photo[-1].file_id,
        caption=text,
        reply_markup=tmoder.virtual_kb(ctx.from_user.id)
    )

    await state.set_state(None)


    db.add(SubscribeTable(
        user_id=user_id,
        active=False,
        expire_data=expire_date
    ))

    await db.commit()


async def virtual_cancel_handler(
    ctx : Message, 
    state : FSMContext, 
    db : AsyncSession
):
    """
    
    Virtual paid

    """
    
    await bot.send_message(
        chat_id=ctx.from_user.id,
        text=tstart.text,
        reply_markup=tstart.kb
    )


    await state.set_state(None)

    await db.close()





async def virtual_paid_raiting(
    ctx : Message, 
    state : FSMContext, 
    db : AsyncSession
):

    await ctx.answer(
        text=tvirtual.paid_raiting,
        reply_markup=tstart.kb
    )

    data = await state.get_data()
    
    from_id = int(data.get("from_id"))
    to_id = int(data.get("to_id"))
    page = int(data.get("page"))

    chat_id = ctx.from_user.id

    if page < 0:
        app = await ubase.get_app(db, chat_id)


        if app is None:
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

    else:
        app = await ubase.get_app(db, to_id)
        await Upremium.send_app_premium(chat_id, app, page)

    await state.set_state(None)

    photo_id = await ubase.get_save_photo_id(ctx)


    caption = tvirtual.check_raiting.format(
        from_id=from_id,
        username=ctx.from_user.username,
        to_id=to_id,
    )


    await bot.send_photo(
        chat_id=config.MODER_GROUP,
        caption=caption,
        photo=photo_id,
        reply_markup=tmoder.raiting_kb(from_id, to_id, page)
    )

    await db.close()


async def virtual_cancel_raiting(
    ctx : CallbackQuery, 
    state : FSMContext, 
    db : AsyncSession
):

    chat_id = ctx.from_user.id
    data = await state.get_data()

    from_id = int(data.get("from_id"))
    to_id = int(data.get("to_id"))
    page = int(data.get("page"))


    if page < 0:


        app = await ubase.get_app(db, chat_id)


        if app is None:
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
    else:
        app = await ubase.get_app(db, to_id)
        await Upremium.send_app_premium(chat_id, app, page)


    await state.set_state(None)



@dp.callback_query_handler(
    mpayemnt.PaymentCall.filter(action="pay")
)
async def payment_handler(
    ctx : CallbackQuery,
    callback_data : dict,
    state : FSMContext
):
    data = await state.get_data()

    paid_function = callback_data.get("paid_function")
    cancel_function = callback_data.get("cancel_function")
    paid_info = data.get("paid_info")

    await ctx.message.delete()

    if paid_info == "premium":
        message = await ctx.message.answer(
            text=tpayment.premium_payment_data,
            reply_markup=tpayment.kb_cancel,
            parse_mode="MARKDOWN"
        )
    else:
        message = await ctx.message.answer(
            text=tpayment.payment_data,
            reply_markup=tpayment.kb_cancel,
            parse_mode="MARKDOWN"
        )

    await state.update_data(
        paid_function=paid_function,
        cancel_function=cancel_function,
        payment_message_id = message.message_id,
        paid_data= callback_data.get("data"),
    )


    await state.set_state(mpayemnt.PaymentState.payment)


@dp.message_handler(
    state=mpayemnt.PaymentState.payment,
    content_types=ContentTypes.PHOTO
)
async def paid_handler(
    ctx : Message,
    state : FSMContext,
    db : AsyncSession
):
    data = await state.get_data()

    paid_function = data.get("paid_function")
    payment_message_id = data.get("payment_message_id")

    if not paid_function:
        print("err")


    await bot.delete_message(
        chat_id=ctx.chat.id,
        message_id=payment_message_id,
    )

    await ctx.delete()

    await globals()[paid_function](ctx, state, db) 


@dp.callback_query_handler(
    mpayemnt.PaymentCall.filter(action="cancel"),
    state=None
)
async def cancel_query_handler(
    ctx : CallbackQuery,
    callback_data : dict,
    state : FSMContext,
    db : AsyncSession
):
    cancel_function = callback_data.get("cancel_function")

    await ctx.message.delete()

    await globals()[cancel_function](ctx, state, db) 


@dp.message_handler(
    Text(tpayment.payment_btn_cancel),
    state=mpayemnt.PaymentState.payment
)
async def cancel_message_handler(
    ctx : Message,
    state : FSMContext,
    db : AsyncSession
):
    data = await state.get_data()
    cancel_function = data.get("cancel_function")
    payment_message_id = data.get("payment_message_id")

    await ctx.delete()
    await bot.delete_message(ctx.from_user.id, payment_message_id)

    await globals()[cancel_function](ctx, state, db) 



