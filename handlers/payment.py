import os
from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from database import get_user_data


# Holatlarni shu yerning o'zida aniqlaymiz
class PaymentStates(StatesGroup):
    wait_for_check = State()


router = Router()

# O'zingizning ID'ingizni yozing (chek sizga kelishi uchun)
ADMIN_ID = 123456789


@router.message(F.text == "💰 Balans / Referal 👥")
async def show_balance_menu(message: types.Message):
    user_id = message.from_user.id
    data = get_user_data(user_id)
    balance = data[0] if data else 0

    bot_username = (await message.bot.get_me()).username
    referral_link = f"https://t.me/{bot_username}?start={user_id}"

    text = (
        f"👤 **Foydalanuvchi:** {message.from_user.full_name}\n"
        f"💰 **Sizning balansingiz:** {balance} so'm\n\n"
        f"👥 **Referal tizimi:**\n"
        f"Do'stlarni taklif qiling va har biriga 500 so'm bonus oling!\n\n"
        f"🔗 Referal havolangiz:\n`{referral_link}`"
    )

    kb = [
        [types.InlineKeyboardButton(text="💳 Balansni to'ldirish", callback_data="fill_balance")],
        [types.InlineKeyboardButton(text="📈 Referallarim", callback_data="my_refs")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")


@router.callback_query(F.data == "fill_balance")
async def fill_balance_info(callback: types.CallbackQuery, state: FSMContext):
    payment_text = (
        "💳 **Balansni to'ldirish tartibi:**\n\n"
        "1. Karta: `8600000000000000` (Ism Familiya)\n"
        "2. To'lovdan so'ng **chek rasmini** yuboring.\n\n"
        "Hozir chek rasmini yuborishingizni kutyapman..."
    )
    # Botni "chek kutish" holatiga o'tkazamiz
    await state.set_state(PaymentStates.wait_for_check)
    await callback.message.answer(payment_text, parse_mode="Markdown")
    await callback.answer()


# FAQAT wait_for_check holatida rasm kelsa ishlaydi
@router.message(PaymentStates.wait_for_check, F.photo)
async def handle_check_sent(message: types.Message, state: FSMContext, bot: Bot):
    # Foydalanuvchiga javob
    await message.answer("✅ Rahmat! Chekingiz adminga yuborildi. Tekshiruvdan so'ng pul balansingizga qo'shiladi.")

    # Adminga yuborish (Tasdiqlash tugmasi bilan)
    builder = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="✅ Tasdiqlash (5000 so'm)", callback_data=f"confirm_{message.from_user.id}")]
    ])

    await bot.send_photo(
        chat_id=ADMIN_ID,
        photo=message.photo[-1].file_id,
        caption=f"💰 **Yangi to'lov cheki!**\nUser: {message.from_user.full_name}\nID: `{message.from_user.id}`",
        reply_markup=builder,
        parse_mode="Markdown"
    )

    # Holatni tozalaymiz (endi rasm yuborsa OCR ishlayveradi)
    await state.clear()


@router.message(PaymentStates.wait_for_check)
async def not_a_photo(message: types.Message):
    await message.answer("Iltimos, to'lov chekini **rasm (photo)** ko'rinishida yuboring.")