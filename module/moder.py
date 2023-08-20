from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters.state import (
    StatesGroup, State
)


ClubCall = CallbackData(
    "club-moder",
    "action",
    "gender",
    "user_id",
)


VirtualCall = CallbackData(
    "virtual-moder",
    "action",
    "user_id"
)


ModerCall = CallbackData(
    "moder", 
    "action", 
    "user_id"
)

PaymentCall = CallbackData(
    "payment-moder",
    "action",
    "from_id",
    "to_id",
    "page"
)

class PaymentState(StatesGroup):

    count = State()