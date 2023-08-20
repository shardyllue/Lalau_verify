from asyncio import gather, create_task

from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from core import dp
from db import AsyncSession
from db.base import AppTable


from utils import base as Ubase
from utils import valid as Uvalid
from utils.app import send_app



from module.register import RegisterState


import template.base as Tbase
import template.register as tregister
import template.start as tstart
import utils.moder as umoder




async def send_user_app(
    db : AsyncSession,
    ctx : types.Message, 
    app : AppTable,
    state : FSMContext
):
    await ctx.answer(
        text=tregister.success,
        reply_markup=tstart.kb
    )


    await umoder.moderate(
        user=app,
        db=db
    )

    _app = await send_app(
        chat_id = ctx.from_user.id,
        app=app
    )


    return await gather(
        create_task(db.commit()),
        create_task(state.update_data(app_id=_app.message_id)),
        create_task(state.set_state(None)),
    )


@dp.message_handler(
    Text([Tbase.back_text]),
    state=RegisterState
)
async def comeback_handler(
    ctx : types.Message,
    db : AsyncSession,
    state : FSMContext
):
    """

    Handler for comebacking
    
    """
    reponse = await gather(
        create_task(state.get_state()),
        create_task(state.get_data())
    )

    current_state = reponse[0]
    name = reponse[1].get("name")

    
    if (
        (current_state == RegisterState.form.state) or
        (current_state == RegisterState.name.state)
    ):
        return await gather(
            create_task(db.close()),
            create_task(state.set_state(None)),
            create_task(ctx.answer(
                text=tstart.text,
                reply_markup=tstart.kb
            ))
        )

    elif current_state == RegisterState.name.state:
        return await gather(
            create_task(db.close()),
            create_task(RegisterState.gender.set()),
            create_task(ctx.answer(
                text=tregister.gender_text,
                reply_markup=tregister.gender_kb
            ))
        )
    elif current_state == RegisterState.years.state:
        return await gather(
            create_task(db.close()),
            create_task(RegisterState.name.set()),
            create_task(ctx.answer(
                text=tregister.name,
                reply_markup=tregister.back_kb
            ))
        )
    elif current_state == RegisterState.city.state:
        return await gather(
            create_task(db.close()),
            create_task(RegisterState.years.set()),
            create_task(ctx.answer(
                text=tregister.years.format(name=name),
                reply_markup=tregister.back_kb
            ))
        )
    elif current_state == RegisterState.usr.state:
        return await gather(
            create_task(db.close()),
            create_task(RegisterState.city.set()),
            create_task(ctx.answer(
                text=tregister.city,
                reply_markup=tregister.back_kb
            ))
        )
    elif current_state == RegisterState.photo.state:
        return await gather(
            create_task(db.close()),
            create_task(RegisterState.usr.set()),
            create_task(ctx.answer_photo(
                photo=tregister.usr_photo,
                caption=tregister.usr_text,
                reply_markup=tregister.usr_kb
            ))
        )
    elif current_state == RegisterState.video.state:
        return await gather(
            create_task(db.close()),
            create_task(RegisterState.photo.set()),
            create_task(ctx.answer(
                text=tregister.photo_text,
                reply_markup=tregister.photo_kb
            ))
        )

    elif current_state == RegisterState.pub_video.state:
        return await gather(
            create_task(db.close()),
            create_task(RegisterState.video.set()),
            create_task(ctx.answer(
                text=tregister.video_text,
                reply_markup=tregister.video_kb
            ))
        )

    return await db.close()


@dp.message_handler(
    Text(tregister.register_btn_yes),
    state=RegisterState.form
)
async def register_gender_handler(
    ctx : types.Message,
    db : AsyncSession,
):
    """
    App main.

    give a ppp to users
    """
    await ctx.answer(
        text=tregister.name,
        reply_markup=tregister.back_kb
    )

    return await gather(
        create_task(db.close()),
        create_task(RegisterState.name.set())
    )


@dp.message_handler(
    content_types=types.ContentTypes.TEXT,
    state=RegisterState.name
)
async def register_name_handler(
    ctx : types.Message,
    db : AsyncSession,
    state : FSMContext
):
    """
    App main.

    give a ppp to users
    """

    if not Uvalid.valid_name(name:=ctx.text):
        return await gather(
            create_task(db.close()),
            create_task(ctx.delete()),
            create_task(Ubase.delay(
                ctx.answer(tregister.err_name))
            ),
        )

    await ctx.answer(
        text=tregister.years.format(name=ctx.text),
        reply_markup=tregister.back_kb
    )

    return await gather(
        create_task(db.close()),
        create_task(state.update_data(name=name)),
        create_task(RegisterState.years.set())
    )


@dp.message_handler(
    content_types=types.ContentTypes.TEXT,
    state=RegisterState.years
)
async def register_years_handler(
    ctx : types.Message,
    db : AsyncSession,
    state : FSMContext
):
    """
    App main.

    give a ppp to users
    """

    if not Uvalid.valid_years(years:=ctx.text):
        return await gather(
            create_task(db.close()),
            create_task(ctx.delete()),
            create_task(Ubase.delay(
                ctx.answer(tregister.err_years))
            ),
        )


    await ctx.answer(
        text=tregister.city,
        reply_markup=tregister.back_kb
    )

    return await gather(
        create_task(db.close()),
        create_task(state.update_data(years=int(years))),
        create_task(RegisterState.city.set())
    )


@dp.message_handler(
    content_types=types.ContentTypes.TEXT,
    state=RegisterState.city
)
async def register_city_handler(
    ctx : types.Message,
    db : AsyncSession,
    state : FSMContext
):
    """
    App main.

    give a ppp to users
    """
    
    if not Uvalid.valid_city(city:=ctx.text):
        return await gather(
            create_task(db.close()),
            create_task(ctx.delete()),
            create_task(Ubase.delay(ctx.answer(tregister.err_city))
            ),
        )

    await ctx.answer_photo(
        photo=tregister.usr_photo,
        caption=tregister.usr_text,
        reply_markup=tregister.usr_kb
    )

    return await gather(
        create_task(db.close()),
        create_task(state.update_data(city=city)),
        create_task(RegisterState.usr.set())
    )


@dp.message_handler(
    content_types=types.ContentTypes.TEXT,
    state=RegisterState.usr
)
async def register_usrname_handler(
    ctx : types.Message,
    db : AsyncSession,
    state : FSMContext
):
    """
    App main.

    give a ppp to users
    """
    #Check if use want using default name from telegram
    if (usrname:=ctx.text) == tregister.usr_username_btn:
        #If telegram's user is Nonw
        if (usr_tg:=ctx.from_user.username) is None:
            return await gather(
                create_task(db.close()),
                create_task(ctx.delete()),
                create_task(Ubase.delay(
                    ctx.answer(tregister.usr_err))
                )
            )
        
        usrname = "@" + usr_tg
    #Validate usrname from user
    elif not Uvalid.valid_usr(usrname):
        return await gather(
            create_task(db.close()),
            create_task(ctx.delete()),
            create_task(Ubase.delay(ctx.answer(tregister.usr_err))),
        )



    await ctx.answer(
        text=tregister.photo_text,
        reply_markup=tregister.photo_kb
    )

    return await gather(
        create_task(db.close()),
        create_task(state.update_data(usrname=usrname)),
        create_task(RegisterState.photo.set())
    )


@dp.message_handler(
    content_types=types.ContentTypes.PHOTO,
    state=RegisterState.photo
)
async def register_photo_handler(
    ctx : types.Message,
    db : AsyncSession,
    state : FSMContext
):
    """
    App main.

    give a ppp to users
    """

    data = await state.get_data()

    photo_id = await Ubase.get_save_photo_id(ctx)


    await ctx.answer(
        text=tregister.video_text,
        reply_markup=tregister.video_kb
    )


    return await gather(
        create_task(db.close()),
        create_task(state.update_data(photo_id=photo_id)),
        create_task(RegisterState.video.set())
    )



@dp.message_handler(
    content_types=types.ContentTypes.VIDEO_NOTE,
    state=RegisterState.video
)
async def register_video_handler(
    ctx : types.Message,
    db : AsyncSession,
    state : FSMContext
):
    """
    App main.

    give a ppp to users
    
    """
    data = await state.get_data()
    chat_id = ctx.from_user.id

    video_id = await Ubase.get_save_video_id(ctx)

    await ctx.answer(
        text=tregister.pub_video_text,
        reply_markup=tregister.pub_video_kb
    )


    return await gather(
        create_task(db.close()),
        create_task(state.update_data(video_id=video_id)),
        create_task(RegisterState.pub_video.set())
    )


@dp.message_handler(
    Text([
        tregister.pub_video_accept_btn, 
        tregister.pub_video_dicline_btn
    ]),
    state=RegisterState.pub_video
)
async def register_finish_handler(
    ctx : types.Message,
    db : AsyncSession,
    state : FSMContext
):
    data = await state.get_data()
    chat_id = ctx.chat.id

    if ctx.text == tregister.pub_video_accept_btn:
        pub_video = True
    else:
        pub_video = False

    db.add(app:=AppTable(
        chat_id=chat_id,
        gender="Девушка",
        name=data.get("name"),
        years=data.get("years"),
        city=data.get("city"),
        usrname=data.get("usrname"),
        photo_id=data.get("photo_id"),
        video_id=data.get("video_id"),
        pub_video=pub_video,
        moderated=False
    ))

    return await send_user_app(db, ctx, app, state)
