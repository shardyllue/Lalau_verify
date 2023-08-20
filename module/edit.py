from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters.state import (
    StatesGroup, State
)

EditCall = CallbackData(
    "app.edit", 
    "value"
)


class EditState(StatesGroup):

    name = State()
    years = State()
    city = State()
    usrname = State()
    photo = State()
    video = State()