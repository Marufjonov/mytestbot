import os
from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from states.states import UserState  # Holatlarni import qilamiz
from utils.ai.gemini_client import GeminiClient

router = Router()
ai_client = GeminiClient()


# 1. Tugma bosilganda holatni o'zgartirish
@router.message(F.text == "📸 Rasm yuborish")
async def start_ocr_process(message: types.Message, state: FSMContext):
    await message.answer("Matnini ajratib olmoqchi bo'lgan rasmingizni yuboring:")
    # Botni "rasm kutish" holatiga o'tkazamiz
    await state.set_state(UserState.wait_photo)


# 2. Faqat wait_photo holatida rasm kelsa ishlov berish
@router.message(UserState.wait_photo, F.photo)
async def handle_photo(message: types.Message, bot: Bot, state: FSMContext):
    wait_msg = await message.answer("📸 Rasm qabul qilindi. Matn ajratilmoqda...")

    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)

    os.makedirs("files", exist_ok=True)
    image_path = f"files/{photo.file_id}.jpg"

    await bot.download_file(file.file_path, image_path)

    try:
        extracted_text = await ai_client.process_image(image_path)

        if not extracted_text or extracted_text.strip() == "":
            await message.answer("Rasmda hech qanday matn aniqlanmadi.")
            return

        result_filename = f"files/text_{message.from_user.id}.txt"
        with open(result_filename, "w", encoding="utf-8") as f:
            f.write(extracted_text)

        document = types.FSInputFile(result_filename)
        await message.answer_document(
            document,
            caption="✅ Rasmdagi barcha matnlar .txt formatida ajratildi."
        )

        # Jarayon tugagach holatni tozalaymiz
        await state.clear()

    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {str(e)}")
    finally:
        if os.path.exists(image_path):
            os.remove(image_path)
        if 'result_filename' in locals() and os.path.exists(result_filename):
            os.remove(result_filename)
        await wait_msg.delete()