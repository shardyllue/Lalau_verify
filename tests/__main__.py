from asyncio import run, create_task, gather
from random import randint, choice

from db import Session, AsyncSession
from db.base import AppTable

async def generate_data(db : AsyncSession):
    db.add(AppTable(
        chat_id=randint(10000, 99999),
        gender=choice(["Мужчина", "Девушка"]),
        years=randint(18, 50),
        name=str(randint(10000, 99999)),
        city=str(randint(10000, 99999)),
        usrname="@" + str(randint(10000, 99999)),
        photo_id=None,
        video_id=None,
        pub_video=False,
        moderated=True
    ))

    return await db.commit()


async def main():
    
    tasks = []

    for _ in range(0, 255):
        tasks.append(create_task(
            generate_data(Session())
        ))

    await gather(*tasks)




if __name__ == "__main__":
    run(main())
