from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, Command
#
from loader import bot, router_user
from keyboards.default.main import *


class Information(StatesGroup):
    ariza = State()
    fullname = State()
    technologies = State()
    phone_number = State()
    location = State()
    price = State()
    user_job = State()
    time = State()
    goal = State()

ADMIN = 5471452269

@router_user.message(CommandStart())
async def start(msg: Message, state: FSMContext):
    if msg.from_user.id == ADMIN:
        await msg.answer('Assalomu aleykum Admin!')
    else:
        await state.set_state(Information.ariza)
        await msg.answer(f"Assalom alaykum {msg.from_user.full_name}\nUstozShogird kanalining rasmiy botiga xush kelibsiz!", reply_markup=menu)