import datetime as dt
from asyncio import sleep

from core import dp, bot, mute_storage
from aiogram.types import Message, ContentTypes, ChatPermissions
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import CantRestrictChatOwner

from db import AsyncSession

from utils.base import link_kb

import utils.config as config
import template.start as Tstart
import template.channel as tchannel


@dp.message_handler(commands=["post"])
async def post_channel_handler(
    ctx : Message,
    db : AsyncSession
):
    
    if ctx.chat.id != config.MODER_GROUP:
        return await db.close()
    
    me = await bot.get_me()

    await bot.send_message(
        chat_id=config.PUBLIC_GROUP,
        text=Tstart.Channel.text,
        reply_markup=Tstart.Channel.kb(me.username)
    )

    return await db.close()



@dp.message_handler(commands=["mute"])
async def add_word_to_mute(ctx : Message):

    if ctx.chat.id != config.MODER_GROUP:
        return

    args = ctx.get_args().split(sep=" ")

    command = args[0]
    args = args[1:]



    if command == "add":

        words = ""

        for word in args:

            word = word.lower()
            mute_storage.add(word)
            words += word + ", "

           
        await ctx.answer(
            text=tchannel.mute_add.format(word=words)
        )

        return
    
    elif command == "remove":
        
        words = ""

        for word in args:

            word = word.lower()
            mute_storage.remove(word)
            words += word + ", "

           
        await ctx.answer(
            text=tchannel.mute_remove.format(word=words)
        )
    
        return
    
    data = mute_storage.words


    words = ""

    for word in data:
        words += word + ", "


    await ctx.answer(
        text=tchannel.mute_list.format(words=words),
    )
     


    

    


    
# @dp.message_handler(commands=["mute"])
# async def add_word_to_mute(ctx : Message):
    
#     data = mute_storage.words


#     text_words = ""

#     for word in data:
#         text_words += word + ", "


#     await ctx.answer(
#         text=text_words,
#     )
    



@dp.message_handler(content_types=ContentTypes.TEXT)
async def moderate_message(ctx : Message, state : FSMContext):


    if ctx.chat.id != config.PUBLIC_GROUP:
        return

    words = ctx.text.lower().split(sep=" ")

    count_mute_word = 0

    mute_words = mute_storage.words

    for word in words:

        if word not in mute_words:
            continue

        count_mute_word += 1


    if count_mute_word == 0:
        return
    
    data = await state.get_data()

    mute_step = data.get("mute_step")


    _bot = await bot.get_me()

    message = await ctx.reply(
        text=tchannel.mute_message,
        reply_markup=link_kb(
            text=tchannel.goto,
            link=f"t.me/{_bot.username}?start=virt"
        )
    ) 

    if not mute_step: 
    
        

        await state.update_data(
            mute_step=True
        )

        return  
    
    
    try:
        return await bot.restrict_chat_member(
            chat_id=config.PUBLIC_GROUP, 
            user_id=ctx.from_user.id,
            permissions=ChatPermissions(False),
            can_send_messages=False,
            until_date=dt.timedelta(days=30)
        )
    except CantRestrictChatOwner:
        ...


    await sleep(5*60)

    try:
        await ctx.delete()
    except:
        ...

    try:
        await message.delete()
    except:
        ...

