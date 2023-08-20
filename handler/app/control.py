from asyncio import gather, create_task

from aiogram import types
from aiogram.dispatcher import FSMContext


from core import dp


from utils import base as Ubase


from db import AsyncSession
from db.sql import delete
from db.base import AppTable

import utils.moder as umoder
import template.app as tapp
import template.edit as Tedit
import template.start as Tstart
import template.virtual as tvirtual
import template.payment as tpayment
import module.app as Mapp


@dp.callback_query_handler(
    Mapp.UserCall.filter(
        action="open.edit"),
    state=None
)
async def open_edit_handler(
    query : types.CallbackQuery,
    callback_data : dict,
    db : AsyncSession,
    state : FSMContext,
) -> None:
    return await gather(
        create_task(db.close()),
        create_task(query.message.edit_reply_markup(
            reply_markup=Tedit.kb
        ))
    )


@dp.callback_query_handler(
    Mapp.UserCall.filter(
        action="open.control"),
    state=None
)
async def open_edit_handler(
    query : types.CallbackQuery,
    callback_data : dict,
    db : AsyncSession,
    state : FSMContext,
) -> None:
    app = await Ubase.get_app(db, query.from_user.id)

    if app is None:
        return await db.close()
    
    if app.moderated is False:
        await umoder.moderate(app, db)

    return await gather(
        create_task(db.close()),
        create_task(query.message.edit_reply_markup(
            reply_markup=tapp.app_kb(app)
        ))
    )


@dp.callback_query_handler(
    Mapp.UserCall.filter(
        action="delete"),
    state=None,
)
async def delete_app_handler(
    query : types.CallbackQuery,
    callback_data : dict,
    db : AsyncSession,
    state : FSMContext,
) -> None:
    """
    Delete user's app
    """
    user_id = query.from_user.id 
    await db.execute(
        delete(AppTable).where(
            AppTable.user_id == user_id
        )
    )

    return await gather(
        create_task(query.message.delete()),
        create_task(db.commit()),
        create_task(query.message.answer(
            text=tapp.app_delete, 
            reply_markup=Tstart.kb
        ))
    )


@dp.callback_query_handler(
    Mapp.UserCall.filter(action="open.video"), 
    state=None
)
async def open_video_handler(
    query : types.CallbackQuery,
    db : AsyncSession,
    state : FSMContext
):
    app = await Ubase.get_app(db,  query.from_user.id)

    if app is None:
        return await db.close()

    await gather(
        create_task(query.answer(tapp.video_text)),
        create_task(query.message.answer_video_note(
            video_note=app.video_id,
            reply_markup=tapp.video_kb
        ))
    )

    return await db.close()


@dp.callback_query_handler(
    Mapp.UserCall.filter(action="close.video"), 
    state="*"
)
async def close_video_handler(
    query : types.CallbackQuery,
    db : AsyncSession,
    state : FSMContext
):

    return await gather(
        create_task(db.close()),
        create_task(query.message.delete()),
    )


@dp.callback_query_handler(
    Mapp.UserCall.filter(
        action="pay_raiting"),
    state=None,
)
async def raiting(
    ctx : types.CallbackQuery,
    state : FSMContext
):
    
    await ctx.message.delete()

    data = {
        "from_id" : ctx.from_user.id,
        "to_id" : ctx.from_user.id,
        "page" : -1
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