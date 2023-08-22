from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from core import dp

from db import AsyncSession

from module.premium import premiumCall, ChannelState
from utils.base import link_kb


import template.start as tstart
import template.premium as tpremium
import template.payment as tpayment


@dp.message_handler(Text(tstart.PremiunBtn))
async def premium_channel(
    ctx : Message,
    state : FSMContext,
    db : AsyncSession
):   
    await ctx.answer(
        text=tpremium.channel_text,
        reply_markup=tpremium.channel_kb
    )

    await db.close()





@dp.callback_query_handler(
    premiumCall.filter(action=tpremium.channel_btn_womam),
)
async def female_handler(
    ctx : CallbackQuery,
    state : FSMContext,
    db : AsyncSession
):
    

    await ctx.message.edit_text(
        text=tpremium.channel_response_woman.format(
            ctx=ctx
        ),
        reply_markup=link_kb(
            text=tpremium.channel_link_womam_text,
            link=tpremium.channel_link_admin
        )
    )

    await state.set_state(None)

    await db.close()


@dp.callback_query_handler(
    premiumCall.filter(action=tpremium.channel_btn_man),
)
async def male_handler(
    ctx : CallbackQuery,
    state : FSMContext,
    db : AsyncSession
):
    

    markup = await tpayment.pay(
        paid_function="premium_paid_channel", 
        cancel_function="premium_cancel_channel",
        state=state,
        data={
            "paid_info" : "premium"
        }
    )

    await ctx.message.edit_text(
        text=tpremium.channel_response_man_2,
        reply_markup=markup
    )

    await state.set_state(None)

    await db.close()
