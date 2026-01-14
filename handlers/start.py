from aiogram import Router, types
from aiogram.filters import CommandStart
from database import add_user, get_balance

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    # Referal ID ni aniqlash (masalan: t.me/bot?start=12345)
    args = message.text.split()
    referrer_id = int(args[1]) if len(args) > 1 and args[1].isdigit() else None

    add_user(user_id, message.from_user.username, referrer_id)

    # Yangilangan asosiy menu tugmalari
    kb = [
        [
            types.KeyboardButton(text="📸 Rasm yuborish"),
            types.KeyboardButton(text="📄 PDF yuborish")
        ],
        [types.KeyboardButton(text="💰 Balans / Referal 👥")],
        [types.KeyboardButton(text="ℹ️ Yordam")]
    ]

    # resize_keyboard=True tugmalarni chiroyli va ixcham qiladi
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Kerakli xizmatni tanlang..."
    )

    await message.answer(
        f"Xush kelibsiz, {message.from_user.full_name}!\n\n"
        "Botdan foydalanish uchun quyidagi tugmalardan birini tanlang:",
        reply_markup=keyboard
    )