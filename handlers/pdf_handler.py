import os
from aiogram import Router, types, F, Bot
from utils.ai.gemini_client import GeminiClient

router = Router()
ai_client = GeminiClient()


@router.message(F.document)
async def handle_pdf_document(message: types.Message, bot: Bot):
    if message.document.mime_type != "application/pdf":
        await message.answer("Iltimos, faqat PDF yuboring.")
        return

    # Foydalanuvchi balansini tekshirish (masalan, 1 ta PDF = 500 so'm)
    # Bu yerda balansni tekshirish kodi bo'ladi (database.py orqali)

    wait_msg = await message.answer("Skanerlangan fayl tahlil qilinmoqda. Bu biroz vaqt olishi mumkin...")

    file_id = message.document.file_id
    file = await bot.get_file(file_id)

    # Files papkasini tekshirish
    os.makedirs("files", exist_ok=True)
    temp_path = f"files/{file_id}.pdf"

    await bot.download_file(file.file_path, temp_path)

    try:
        # Gemini-ning o'zi PDF-ni ko'rib, matnini yozib beradi
        final_text = await ai_client.process_scanned_pdf(temp_path)

        # Natijani faylga yozish
        result_filename = f"files/result_{message.from_user.id}.txt"
        with open(result_filename, "w", encoding="utf-8") as f:
            f.write(final_text)

        await message.answer_document(
            types.FSInputFile(result_filename),
            caption="✅ Skanerlangan PDF-dan ajratilgan matn."
        )

    except Exception as e:
        await message.answer(f"Xatolik: {e}")

    finally:
        if os.path.exists(temp_path): os.remove(temp_path)
        if 'result_filename' in locals() and os.path.exists(result_filename):
            os.remove(result_filename)
        await wait_msg.delete()