from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram import F
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

@router_user.message(Information.ariza)
async def ariza_state(msg: Message, state: FSMContext):
    await state.update_data(ariza=msg.text)
    await msg.answer("Hozir sizga birnecha savollar beriladi.\nHar biriga javob bering.\nOxirida agar hammasi to`g`ri bo`lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi.")
    await state.set_state(Information.fullname)
    await msg.answer("Ism, familiyangizni kiriting?")

@router_user.message(Information.fullname)
async def fullname_state(msg: Message, state: FSMContext):
    await state.update_data(fullname=msg.text)
    await state.set_state(Information.technologies)
    await msg.answer("📚 Texnologiya:\n\nTalab qilinadigan texnologiyalarni kiriting?\nTexnologiya nomlarini vergul bilan ajrating. Masalan,\n\nJava, C++, C#")

@router_user.message(Information.technologies)
async def technologies_state(msg: Message, state: FSMContext):
    await state.update_data(technologies=msg.text)
    await state.set_state(Information.phone_number)
    await msg.answer("📞 Aloqa:\n\nBog`lanish uchun raqamingizni kiriting?\nMasalan, +998 90 123 45 67")

@router_user.message(Information.phone_number)
async def phone_number_state(msg: Message, state: FSMContext):
    await state.update_data(phone_number=msg.text)
    await state.set_state(Information.location)
    await msg.answer("🌐 Hudud:\n\nQaysi hududdansiz?\nViloyat nomi, Toshkent shahar yoki Respublikani kiriting.")

@router_user.message(Information.location)
async def location_state(msg: Message, state: FSMContext):
    await state.update_data(location=msg.text)
    await state.set_state(Information.price)
    await msg.answer("💰 Narxi:\n\nTolov qilasizmi yoki Tekinmi?\nKerak bo`lsa, Summani kiriting?")

@router_user.message(Information.price)
async def price_state(msg: Message, state: FSMContext):
    await state.update_data(price=msg.text)
    await state.set_state(Information.user_job)
    await msg.answer("👨🏻‍💻 Kasbi: \n\nIshlaysizmi yoki o`qiysizmi?\nMasalan, Talaba")

@router_user.message(Information.user_job)
async def user_job_state(msg: Message, state: FSMContext):
    await state.update_data(user_job=msg.text)
    await state.set_state(Information.time)
    await msg.answer("🕰 Murojaat qilish vaqti: \n\nQaysi vaqtda murojaat qilish mumkin?\nMasalan, 9:00 - 18:00")

@router_user.message(Information.time)
async def time_state(msg: Message, state: FSMContext):
    await state.update_data(time=msg.text)
    await state.set_state(Information.goal)
    await msg.answer("🔎 Maqsad: \n\nMaqsadingizni qisqacha yozib bering.")

@router_user.message(Information.goal)
async def goal_state(msg: Message, state: FSMContext):
    await state.update_data(goal=msg.text)
    data = await state.get_data()
    print(data)

    # Ma'lumotlarni olish (xatoliklarni hisobga olgan holda)
    ariza = data.get('ariza', 'Nomaʼlum')
    fullname = data.get('fullname', 'Nomaʼlum')
    technologies = data.get('technologies', 'Nomaʼlum')
    username = msg.from_user.username
    phone_number = data.get('phone_number', 'Nomaʼlum')
    location = data.get('location', 'Nomaʼlum')
    price = data.get('price', 'Nomaʼlum')
    user_job = data.get('user_job', 'Nomaʼlum')
    time = data.get('time', 'Nomaʼlum')
    goal = data.get('goal', 'Nomaʼlum')

    # Shablon yaratish
    ariza_template = (
        f"{ariza}:\n\n"
        f"🏅 Sherik: {fullname}\n"
        f"📚 Texnologiya: {technologies}\n"
        f"🇺🇿 Telegram: @{username}\n"
        f"📞 Aloqa: {phone_number}\n"
        f"🌐 Hudud: {location}\n"
        f"💰 Narxi: {price}\n"
        f"👨🏻‍💻 Kasbi: {user_job}\n"
        f"🕰 Murojaat qilish vaqti: {time}\n"
        f"🔎 Maqsad: {goal}"
    )

    # Foydalanuvchi va admin ga xabar yuborish
    await msg.answer(ariza_template)
    await bot.send_message(ADMIN, ariza_template)
    await state.clear()