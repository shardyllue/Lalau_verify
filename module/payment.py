from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters.state import (
    StatesGroup, State
)


PaymentCall = CallbackData(
    "payment",
    "action",
    "paid_function",
    "cancel_function"
)


class PaymentState(StatesGroup):

    payment = State()



UserCall = CallbackData(
    "payment", 
    "action", 
    "from_id", 
    "to_id", 
    "page"
)



class UserState(StatesGroup):


    payment = State()
    data = State()
