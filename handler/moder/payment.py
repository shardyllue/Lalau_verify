from core import dp, bot
from asyncio import gather, create_task

from utils import config

from aiogram import types
from aiogram.dispatcher import filters
from aiogram.dispatcher import FSMContext

from db import AsyncSession
from db.sql import update
from db.base import AppTable

import utils.base as Ubase
import template.payment as Tpayment
import template.virtual as tvirtual
import template.moder as Tmoder
import module.moder as Mmoder
import static




@dp.callback_query_handler(
    Mmoder.PaymentCall.filter(action="accept")
)
async def accept_handler(
    query : types.CallbackQuery, 
    callback_data : dict,
    db : AsyncSession, 
    state : FSMContext
):
    """
    Accept handler
    """
    
    from_id = callback_data.get("from_id")
    to_id = callback_data.get("to_id")
    photo_id = query.message.photo[0].file_id

    return await gather(
        create_task(db.close()),
        create_task(Mmoder.PaymentState.count.set()),
        create_task(query.message.delete()),
        create_task(Ubase.delay(query.message.answer("Отправьте"),time = 20)),
        create_task(state.update_data(from_id=from_id)),
        create_task(state.update_data(to_id=to_id)),
        create_task(state.update_data(photo_id=photo_id))
    )


@dp.callback_query_handler(
    Mmoder.PaymentCall.filter(action="decline")
)
async def decline_handler(
    query : types.CallbackQuery, 
    callback_data : dict,
    db : AsyncSession, 
    state : FSMContext
):
    """
    Decline
    """
    from_id = callback_data.get("from_id")

    send_moder = query.message.edit_reply_markup(
        reply_markup=Tmoder.Payment.kb_transfer_close()
    )

    send_user = bot.send_message(from_id, Tmoder.Payment.cancel_transferred)

    return await gather(
        create_task(db.close()),
        create_task(send_moder),
        create_task(send_user)
    )


@dp.message_handler(
    content_types=types.ContentType.TEXT,
    state=Mmoder.PaymentState.count
)
async def score_handler(
    message : types.Message, 
    db : AsyncSession, 
    state : FSMContext
):
    """
    Score
    """

    try: count = int(message.text)
    except ValueError:
        return await gather(
            create_task(db.close()),
            create_task(Ubase.delay(config.MODER_GROUP, "err")),
            create_task(message.delete())
        )

    async with state.proxy() as data:
        from_id = data.get("from_id")
        to_id = data.get("to_id")
        photo_id = data.get("photo_id")


    await db.execute(
        update(AppTable).where(
            AppTable.user_id == int(to_id)
        ).values(score=AppTable.score + count)
    )


    send_moder = message.answer_photo(
        photo=photo_id,
        caption=tvirtual.check_raiting.format(
            from_id = from_id,
            username = message.from_user.username,
            to_id = to_id,
            ),
        reply_markup=Tmoder.Payment.kb_transfer_score(count)
    )

    send_from = bot.send_message(from_id, Tmoder.Payment.transferred_from)
    send_to = bot.send_message(to_id, Tmoder.Payment.transferred_to.format(score=count))

    return await gather(
        create_task(db.commit()),
        create_task(message.delete()),
        create_task(state.finish()),
        create_task(send_moder),
        create_task(send_from),
        create_task(send_to)
    )




