import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv()


class GeminiClient:
    def __init__(self):
        # API kalitni yuklash
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY .env faylida topilmadi!")

        genai.configure(api_key=api_key)

        # Eng barqaror va tezkor model: gemini-1.5-flash
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    # async def process_scanned_pdf(self, file_path: str) -> str:
    #     """
    #     Skanerlangan PDF faylni yuklaydi va Gemini uni multimodal tahlil qiladi.
    #     """
    #     try:
    #         # Faylni Google serveriga vaqtinchalik yuklash
    #         uploaded_file = genai.upload_file(path=file_path, mime_type="application/pdf")
    #
    #         prompt = (
    #             "Ushbu PDF hujjat skanerlangan rasm yoki matndan iborat. "
    #             "Iltimos, undagi barcha matnlarni aniqlab (OCR), xatolarsiz "
    #             "va asl formatini saqlagan holda matn (TXT) ko'rinishida yozib ber. "
    #             "Hech qanday ortiqcha izoh qo'shma, faqat hujjatdagi matnni qaytar."
    #         )
    #
    #         # Matnni generatsiya qilish
    #         response = self.model.generate_content([uploaded_file, prompt])
    #
    #         # Yuklangan faylni Google serveridan o'chirish (xavfsizlik uchun)
    #         genai.delete_file(uploaded_file.name)
    #
    #         return response.text
    #     except Exception as e:
    #         return f"PDF tahlilida xatolik yuz berdi: {str(e)}"

    async def process_image(self, image_path: str) -> str:
        """
        Rasm ichidagi matnlarni Gemini yordamida ajratib oladi (OCR).
        """
        try:
            # Rasmni Pillow orqali ochish
            img = Image.open(image_path)

            prompt = (
                "Ushbu rasmda ko'ringan barcha matnlarni o'qib, "
                "ularni hech qanday qo'shimcha izohlarsiz va salom-aliklarsiz, "
                "faqat matnning o'zini formatlangan holda qaytar."
            )

            # Rasm va promptni birga yuborish
            response = self.model.generate_content([prompt, img])
            return response.text
        except Exception as e:
            return f"Rasm tahlilida xatolik: {str(e)}"