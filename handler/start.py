from asyncio import gather, create_task
from json import loads, decoder

from aiogram.types import Message
from aiogram.dispatcher import filters
from aiogram.dispatcher import FSMContext
from aiogram.utils.deep_linking import decode_payload

from core import dp
from db import AsyncSession

from utils.base import get_app
from utils.premium import send_app_premium

from handler.virtual import virtual

import template.start as tstart
import template.app as tapp
import template.virtual as tvirtual




@dp.message_handler(
    filters.CommandStart(),
    state="*"
)
async def start_handler(
    ctx : Message,
    db : AsyncSession,
    state : FSMContext,
) -> None:
    """
    
    Handler of StartCommand
    
    """

    if ctx.chat.type != "private":
        return await db.close()
    

    async def send_start_menu(virt = False):

        if virt:
            await ctx.answer(
                text=tstart.virt_text,
                reply_markup=tstart.kb
            )

            await virtual(ctx, db)

        else:
            await ctx.answer(
                text=tstart.text,
                reply_markup=tstart.kb
            )

            await db.close()


        return await create_task(state.set_state(None))

    args = ctx.get_args()

    if args == "":

        return await send_start_menu()
    
    elif args == "virt":

        return await send_start_menu(virt=True)

    try:
        payload = loads(decode_payload(args))
    
    except Exception:

        return await send_start_menu()

    
    user_id = payload.get("user_id")
    page = payload.get("page")
    
    if (user_id is None) and (page is None):
        return await send_start_menu()
    
    app = await get_app(db, user_id)

    await ctx.answer(
        text=tapp.premium_getting,
        reply_markup=tstart.kb,
    )


    if (app is None):
        return await gather(
            create_task(db.close()),
            create_task(ctx.answer(tapp.AppPremium.err))
        )
    

    if (app.moderated is not True):
        return await gather(
            create_task(db.close()),
            create_task(ctx.answer(tapp.AppPremium.err))
        )

    return await gather(
        create_task(db.close()),
        create_task(send_app_premium(ctx.chat.id, app, page))
    )



    


