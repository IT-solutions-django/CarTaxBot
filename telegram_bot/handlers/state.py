from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


class CarDutyCalculation(StatesGroup):
    cost = State()
    engine_volume = State()
    currency = State()
    power = State()
    weight = State()
    age = State()
    engine_type = State()


class ClientContacts(StatesGroup):
    name = State()
    phone = State()