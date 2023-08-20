from aiogram.dispatcher.filters.state import (
    StatesGroup, State
)


class RegisterState(StatesGroup):

    form = State()

    gender = State()
    name = State()
    years = State()
    city = State()
    usr = State()
    photo = State()
    video = State()
    pub_video = State()