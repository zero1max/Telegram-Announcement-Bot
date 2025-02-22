from aiogram import F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from loader import bot, router_user

class Information(StatesGroup):
    fullname = State()
    technologies = State()
    phone_number = State()
    location = State()
    price = State()
    user_job = State()
    time = State()
    goal = State()
    confirm_user = State()
    confirm_admin = State()

ADMIN = 5471452269
CHANNEL_ID = -1002198582108

@router_user.message(F.text == "Sherik kerak")
async def ariza_state(msg: Message, state: FSMContext):
    await state.set_state(Information.fullname)
    await msg.answer("Ism, familiyangizni kiriting:")

@router_user.message(Information.fullname)
async def fullname_state(msg: Message, state: FSMContext):
    fullname = msg.text.strip()
    if len(fullname.split()) < 2:
        await msg.answer("Iltimos, to‘liq ism va familiyangizni kiriting!")
        return
    
    await state.update_data(fullname=fullname)
    await state.set_state(Information.technologies)
    await msg.answer("📚 Texnologiyalarni kiriting (vergul bilan ajrating):")

@router_user.message(Information.technologies)
async def technologies_state(msg: Message, state: FSMContext):
    techs = ", ".join([tech.strip() for tech in msg.text.split(",")])
    await state.update_data(technologies=techs)
    await state.set_state(Information.phone_number)
    await msg.answer("📞 Telefon raqamingizni kiriting:")

@router_user.message(Information.phone_number)
async def phone_number_state(msg: Message, state: FSMContext):
    await state.update_data(phone_number=msg.text.strip())
    await state.set_state(Information.location)
    await msg.answer("🌐 Hududingizni kiriting:")

@router_user.message(Information.location)
async def location_state(msg: Message, state: FSMContext):
    await state.update_data(location=msg.text.strip())
    await state.set_state(Information.price)
    await msg.answer("💰 Narx yoki 'Tekin' deb yozing:")

@router_user.message(Information.price)
async def price_state(msg: Message, state: FSMContext):
    await state.update_data(price=msg.text.strip())
    await state.set_state(Information.user_job)
    await msg.answer("👨‍💻 Kasbingiz:")

@router_user.message(Information.user_job)
async def user_job_state(msg: Message, state: FSMContext):
    await state.update_data(user_job=msg.text.strip())
    await state.set_state(Information.time)
    await msg.answer("🕰 Qaysi vaqtda murojaat qilish mumkin?")

@router_user.message(Information.time)
async def time_state(msg: Message, state: FSMContext):
    await state.update_data(time=msg.text.strip())
    await state.set_state(Information.goal)
    await msg.answer("🔎 Maqsadingizni qisqacha yozing:")

@router_user.message(Information.goal)
async def goal_state(msg: Message, state: FSMContext):
    await state.update_data(goal=msg.text.strip())
    data = await state.get_data()

    ariza_template = (
        f"🏅 Sherik: {data['fullname']}\n"
        f"📚 Texnologiya: {data['technologies']}\n"
        f"🇺🇿 Telegram: @{msg.from_user.username}\n"
        f"📞 Aloqa: {data['phone_number']}\n"
        f"🌐 Hudud: {data['location']}\n"
        f"💰 Narxi: {data['price']}\n"
        f"👨‍💻 Kasbi: {data['user_job']}\n"
        f"🕰 Murojaat qilish vaqti: {data['time']}\n"
        f"🔎 Maqsad: {data['goal']}"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="user_confirm")],
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="user_cancel")]
        ]
    )
    await msg.answer(ariza_template, reply_markup=keyboard)
    await state.set_state(Information.confirm_user)

@router_user.callback_query(F.data == "user_confirm")
async def user_confirm(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(ADMIN, f"📩 Yangi ariza:\n\n{callback.message.text}",
                           reply_markup=InlineKeyboardMarkup(
                               inline_keyboard=[
                                   [InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"admin_confirm_{callback.from_user.id}")],
                                   [InlineKeyboardButton(text="❌ Rad etish", callback_data=f"admin_reject_{callback.from_user.id}")]
                               ]))
    await callback.message.answer("✅ Arizangiz adminga yuborildi!")
    await state.set_state(Information.confirm_admin)

@router_user.callback_query(F.data.startswith("admin_confirm_"))
async def admin_confirm(callback: CallbackQuery):
    user_id = callback.data.split("_")[2]
    await bot.send_message(CHANNEL_ID, f"✅ {callback.message.text}\n\n📢 Bu yerda sherik topishingiz mumkin!")
    await callback.message.edit_text("✅ Ariza tasdiqlandi va kanalga joylashtirildi!")

@router_user.callback_query(F.data.startswith("admin_reject_"))
async def admin_reject(callback: CallbackQuery):
    await callback.message.edit_text("❌ Ariza rad etildi!")
