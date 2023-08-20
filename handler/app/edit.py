from core import dp, bot
from asyncio import gather, create_task

from utils import base as Ubase
from utils import valid as Uvalid
from utils import app as UUapp


from aiogram import types
from aiogram.dispatcher import filters
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound

from db import AsyncSession
from db.sql import update
from db.base import AppTable

import template.app as tapp
import template.edit as tedit
import template.register as tregister
import module.edit as Medit
import static


async def render_current_app(
    db : AsyncSession,
    ctx : types.Message,
    state : FSMContext,
):
    chat_id = ctx.from_user.id

    app, data = await gather(
        create_task(Ubase.get_app(db, chat_id)),
        create_task(state.get_data()),
    )

    if app is None:
        try:
            await bot.delete_message(chat_id, data.get("app_id"))
        except MessageToDeleteNotFound:
            ...

        return await gather(
            create_task(state.set_state(None)),
            create_task(db.close()),
            create_task(ctx.delete()),
        )

    return await gather(
        create_task(db.commit()),
        create_task(state.set_state(None)),
        create_task(ctx.delete()),
        create_task(bot.edit_message_media(
            chat_id=chat_id,
            media=types.InputMediaPhoto(
                app.photo_id if app.photo_id else types.InputFile(static.anon_path),
                caption=tapp.app_text.format(app=app)
            ),
            message_id=data.get("app_id"),
            reply_markup=tedit.kb
        ))
    )


@dp.callback_query_handler(
    Medit.EditCall.filter(),
    state=None
)
async def handler_btn(
    query : types.CallbackQuery,
    callback_data : dict,
    db : AsyncSession,
    state : FSMContext
):
    object = callback_data.get("value")
    user_id = query.message.chat.id
    message_id = query.message.message_id

    if object == "switch.video.off":

        await db.execute(update(AppTable).where(
            AppTable.user_id == user_id
        ).values(pub_video = False))

        app = await Ubase.get_app(db, user_id)

        return await gather(       
            create_task(db.commit()),     
            create_task(state.set_state(None)),
            create_task(query.message.edit_reply_markup(
                reply_markup=tapp.app_kb(app)
            ))
        )

    elif object == "switch.video.on":

        await db.execute(update(AppTable).where(
            AppTable.user_id == user_id
        ).values(pub_video = True))


        app = await Ubase.get_app(db, user_id)

        return await gather(     
            create_task(db.commit()),       
            create_task(state.set_state(None)),
            create_task(query.message.edit_reply_markup(
                reply_markup=tapp.app_kb(app)
            ))
        )
    
    
    if object == "switch.channel.off":

        await db.execute(update(AppTable).where(
            AppTable.user_id == user_id
        ).values(post_app = False))

        app = await Ubase.get_app(db, user_id)

        return await gather(       
            create_task(db.commit()),     
            create_task(state.set_state(None)),
            create_task(query.message.edit_reply_markup(
                reply_markup=tapp.app_kb(app)
            ))
        )

    elif object == "switch.channel.on":

        await db.execute(update(AppTable).where(
            AppTable.user_id == user_id
        ).values(post_app = True))


        app = await Ubase.get_app(db, user_id)

        return await gather(     
            create_task(db.commit()),       
            create_task(state.set_state(None)),
            create_task(query.message.edit_reply_markup(
                reply_markup=tapp.app_kb(app)
            ))
        )



    await gather(
        create_task(state.update_data(app_id = message_id)),
        create_task(db.execute(
            update(AppTable).where(
                AppTable.user_id == user_id
            ).values(moderated = False)
        ))
    )


    if object == "name":
        return await gather(
            create_task(db.commit()),
            create_task(Medit.EditState.name.set()),
            create_task(query.message.edit_reply_markup(
                reply_markup=tedit.title(tedit.edit_title_name)
            ))
        )
    elif object == "years":
        return await gather(
            create_task(db.commit()),
            create_task(Medit.EditState.years.set()),
            create_task(query.message.edit_reply_markup(
                reply_markup=tedit.title(tedit.edit_title_years)
            ))
        )
    elif object == "city":
        return await gather(
            create_task(db.commit()),
            create_task(Medit.EditState.city.set()),
            create_task(query.message.edit_reply_markup(
                reply_markup=tedit.title(tedit.edit_title_city)
            ))
        )
    elif object == "usrname":
        return await gather(
            create_task(db.commit()),
            create_task(Medit.EditState.usrname.set()),
            create_task(query.message.edit_reply_markup(
                reply_markup=tedit.title(tedit.edit_title_usrname)
            ))
        )
    elif object == "photo":
        return await gather(
            create_task(db.commit()),
            create_task(Medit.EditState.photo.set()),
            create_task(query.message.edit_reply_markup(
                reply_markup=tedit.title(tedit.edit_title_photo)
            ))
        )
    elif object == "video":
        return await gather(
            create_task(db.commit()),
            create_task(Medit.EditState.video.set()),
            create_task(query.message.edit_reply_markup(
                reply_markup=tedit.title(tedit.edit_title_video)
            ))
        )



@dp.callback_query_handler(
    Medit.EditCall.filter(
        value="cancel"
    ),
    state=Medit.EditState
)
async def cancel_handler(
    query : types.CallbackQuery,
    callback_data : dict,
    db : AsyncSession,
    state : FSMContext
):
    return await gather(
        create_task(db.close()),
        create_task(state.set_state(None)),
        create_task(query.message.edit_reply_markup(
            reply_markup=tedit.kb
        ))
    )

#Имя
@dp.message_handler(
    state=Medit.EditState.name,
    content_types=types.ContentType.TEXT
)
async def set_name_handler(
    ctx : types.Message, 
    state : FSMContext, 
    db : AsyncSession
):
    """
    
    Setter a name

    """   
    if not Uvalid.valid_name(name:=ctx.text):
        return await gather(
            create_task(ctx.delete()),
            create_task(db.close()),
            create_task(Ubase.delay(ctx.answer(
                text=tregister.err_name
            )))
        )

    await db.execute(
        update(AppTable).where(
            AppTable.user_id == ctx.chat.id
        ).values(name=name)
    )

    return await render_current_app(
        db=db,
        ctx=ctx,
        state=state
    )


#Возрост
@dp.message_handler(
    state=Medit.EditState.years,
    content_types=types.ContentType.TEXT
)
async def set_years_handler(
    ctx : types.Message, 
    state : FSMContext, 
    db : AsyncSession
):
    """
    
    Setter a years

    """   
    
    if not Uvalid.valid_years(years:=ctx.text):


        return await gather(
            create_task(ctx.delete()),
            create_task(db.close()),
            create_task(Ubase.delay(ctx.answer(
                text=tregister.err_years
            )))
        )

    await db.execute(
        update(AppTable).where(
            AppTable.user_id == ctx.from_user.id
        ).values(years=int(years))
    )

    return await render_current_app(
        db=db,
        ctx=ctx,
        state=state
    )



#Город
@dp.message_handler(
    state=Medit.EditState.city,
    content_types=types.ContentType.TEXT
)
async def set_city_handler(
    ctx : types.Message, 
    state : FSMContext, 
    db : AsyncSession
):
    """
    
    Setter a city

    """   
    
    if not Uvalid.valid_city(city:=ctx.text):
        return await gather(
            create_task(ctx.delete()),
            create_task(db.close()),
            create_task(Ubase.delay(ctx.answer(
                text=tregister.err_city
            )))
        )

    await db.execute(
        update(AppTable).where(
            AppTable.user_id == ctx.from_user.id
        ).values(city=city)
    )

    return await render_current_app(
        db=db,
        ctx=ctx,
        state=state
    )


#Имя польхователя
@dp.message_handler(
    state=Medit.EditState.usrname,
    content_types=types.ContentType.TEXT
)
async def set_usrname_handler(
    ctx : types.Message, 
    state : FSMContext, 
    db : AsyncSession
):
    """
    
    Setter a username

    """   
    if not Uvalid.valid_usr(usrname:=ctx.text):
        return await gather(
            create_task(ctx.delete()),
            create_task(db.close()),
            create_task(Ubase.delay(ctx.answer(
                text=tregister.usr_err
            )))
        )

    await db.execute(
        update(AppTable).where(
            AppTable.user_id == ctx.from_user.id
        ).values(usrname=usrname)
    )

    return await render_current_app(
        db=db,
        ctx=ctx,
        state=state
    )



#Фото
@dp.message_handler(
    state=Medit.EditState.photo,
    content_types=types.ContentType.PHOTO
)
async def set_photo_handler(
    ctx : types.Message, 
    state : FSMContext, 
    db : AsyncSession
):    
    """
    
    Setter a photo

    """   
    photo_id = await Ubase.get_save_photo_id(ctx)

    await db.execute(
        update(AppTable).where(
            AppTable.user_id ==  ctx.from_user.id
        ).values(photo_id=photo_id)
    )

    return await render_current_app(
        db=db,
        ctx=ctx,
        state=state
    )


#Видео
@dp.message_handler(
    state=Medit.EditState.video,
    content_types=types.ContentType.VIDEO_NOTE
)
async def set_video_handler(
    ctx : types.Message, 
    state : FSMContext, 
    db : AsyncSession
):
    """
    
    Setter a video

    """    
    video_id = await Ubase.get_save_video_id(ctx)

    await db.execute(
        update(AppTable).where(
            AppTable.user_id == ctx.from_user.id
        ).values(video_id=video_id)
    )

    return await render_current_app(
        db=db,
        ctx=ctx,
        state=state
    )


