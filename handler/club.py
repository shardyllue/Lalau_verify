from aiogram.types import Message, ContentTypes
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from loguru import logger


from core import dp, bot
from utils import config

from module.club import ClubState 

import template.start as tstart
import template.moder as tmoder
import template.club as tclub








@dp.message_handler(Text(tstart.WomenBtn))
async def women_club(ctx : Message, state : FSMContext):
    
    await ctx.answer_photo(
        photo=tclub.women_image(),
        caption=tclub.women_text,
        reply_markup=tclub.kb
    )

    await state.set_state(ClubState.club)
    await state.update_data(club_gender="Девушка")


@dp.message_handler(Text(tstart.MenBtn))
async def women_club(ctx : Message, state : FSMContext):
    
    await ctx.answer_photo(
        photo=tclub.men_image(),
        caption=tclub.men_text,
        reply_markup=tclub.kb
    )

    await state.set_state(ClubState.club)
    await state.update_data(club_gender="Мужчина")



@dp.message_handler(
    Text(tclub.cancel),
    state=ClubState.club
)
async def cancel_handler(
    ctx : Message, 
    state : FSMContext
):

    await ctx.answer(
        text=tstart.text,
        reply_markup=tstart.kb
    )

    await state.set_state(None)



@dp.message_handler(
    content_types=ContentTypes.VIDEO_NOTE,
    state=ClubState.club
)
async def club_handler(
    ctx : Message, 
    state : FSMContext
):

    await ctx.answer(
        text=tclub.moder,
        reply_markup=tstart.kb
    )

    await state.set_state(None)
    

    data = await state.get_data()
    gender = data.get("club_gender")
    

    if not gender:
        logger.error("Not found a club_gender!!!!")
        return
    

    first_name = ctx.from_user.first_name
    last_name = ctx.from_user.last_name
    user_id = ctx.from_user.id
    username = ctx.from_user.username

    if not last_name:
        full_name = first_name

    else:
        full_name = first_name + " " + last_name

    _text = tmoder.club_text.format(
        gender=gender,
        full_name = full_name,
        user_id = user_id,
        username = username,
    )

    _kb = tmoder.club_kb(
        user_id=ctx.from_user.id,
        gender=gender
    )

    await bot.send_video_note(
        video_note=ctx.video_note.file_id,
        chat_id=config.MODER_GROUP,
    )

    await bot.send_message(
        chat_id=config.MODER_GROUP,
        text=_text,
        reply_markup=_kb
    )





    