import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

# Ichki modullarni import qilish
from database import init_db
from handlers import start, payment, pdf_handler, image_handler  # pdf_handler hali bo'sh bo'lsa, buni kommentga oling

# .env faylini yuklash
load_dotenv()


async def main():
    # Loggingni sozlash (xatolarni ko'rish uchun)
    logging.basicConfig(level=logging.INFO)

    # Ma'lumotlar bazasini tayyorlash
    init_db()

    # Bot va Dispatcher obyektlarini yaratish
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    # Routerlarni ulash
    dp.include_router(start.router)
    dp.include_router(payment.router)
    dp.include_router(pdf_handler.router)
    dp.include_router(image_handler.router)
    print("--- Bot muvaffaqiyatli ishga tushdi ---")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot to'xtatildi!")