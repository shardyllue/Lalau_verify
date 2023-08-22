import aioschedule as schedule
import datetime as dt

from loguru import logger
from asyncio import sleep
from datetime import datetime
from core import bot

from random import choice, randint

from db import AsyncSession, async_sessionmaker
from db.sql import select, update, delete
from db.base import AppTable, SubscribeTable

from utils import config

import utils.base as Ubase
from utils.premium import send_app_premium_group

import template.virtual as tvirtual 
import template.channel as tchannel



showen = []


async def main_posting(db : AsyncSession):
    """
    
    Posting to main group
    
    """
    data = datetime.now()

    if not (datetime(data.year, data.month, data.day, 6, 0) < datetime.now() < datetime(data.year, data.month, data.day, 23, 0)):
        return await db.close()
    
    apps = await Ubase.get_apps(db, public=True)
    await db.close()

    if len(apps) == 0:
        return

    
    pages = Ubase.splite_array(apps, 9)
    random_page = randint(0, len(pages)-1)

    async def get_unque():
        random_app = choice(pages[random_page])

        if len(apps) == 0:
            return None

        if len(showen) == len(apps):
            showen.clear()

        if (user:=random_app.user_id) not in showen:
            

            showen.append(user)


            return random_app
        
        return await get_unque()
    
    
    random_app = await get_unque()

    if not random_app:
        logger.info("Posting. No one")
        return

    logger.info("Posting")



        
    return await send_app_premium_group(random_app, random_page)

    
async def sqlachmey_zeroing(
    db : AsyncSession
):
    """
    Set everybody score to 0 
    """

    logger.info("Zeroing")

    sql = update(AppTable).values(score=0)

    await db.execute(sql)

    return await db.commit()


async def public_posting():
    # Отправка поста в группу
    post = await bot.send_message(
        chat_id=config.PUBLIC_GROUP,
        text=tchannel.channel_text,
        reply_markup=tchannel.channel_kb,
        parse_mode="html"
    )

    # Закрепление поста в группе
    await bot.pin_chat_message(chat_id=config.PUBLIC_GROUP, message_id=post.message_id)


async def sqlachmey_check_subs(
    db : AsyncSession
):
    """
    Set everybody score to 0 
    """

    response = await db.execute(select(SubscribeTable))

    subs = [sub[0] for sub in response.fetchall()]

    for sub in subs:

        sub : SubscribeTable

        now = dt.datetime.now()


        if sub.expire_data < dt.datetime.date(now):

            await bot.send_message(
                chat_id=sub.user_id,
                text=tvirtual.subscribe_expired
            )

            logger.warning(f"Subscribe for ID{sub.user_id} was expired. Date: {sub.expire_data}")

            await db.execute(delete(SubscribeTable).where(
                SubscribeTable.user_id == sub.user_id
            ))

    return await db.commit()


async def scheduler_startup(
    async_session : async_sessionmaker
) -> None:
    """
    schedular 
    """

    # schedule.every(30).days.do(
    #     sqlachmey_zeroing, 
    #     db = async_session()
    # )
    schedule.every().day.at("00:01").do(
        sqlachmey_check_subs, 
        db = async_session()
    )
    schedule.every(2).hours.do(
        main_posting, 
        db = async_session()
    )

    schedule.every(5).days.do(public_posting)

    while True:
        await schedule.run_pending()
        await sleep(1)
