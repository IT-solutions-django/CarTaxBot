from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


class CarDutyCalculation(StatesGroup):
    car_type = State() 
    currency = State()
    cost = State()
    engine_volume = State()
    power = State()
    weight = State()
    client_type = State()
    age = State()
    engine_type = State()
    power_known = State()


class ClientContacts(StatesGroup):
    name = State()
    phone = State()