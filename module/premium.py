from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters.state import (
    StatesGroup, State
)



class ChannelState(StatesGroup):


    gender = State()
    info = State()
    payment = State()




bandCall = CallbackData(
    "premium.band", 
    "action", 
    "page"
)

appCall = CallbackData(
    "premium.app", 
    "action", 
    "user_id", 
    "page"
)


premiumCall = CallbackData(
    "premium",
    "action"
)