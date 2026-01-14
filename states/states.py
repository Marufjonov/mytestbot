from aiogram.fsm.state import StatesGroup, State

class UserState(StatesGroup):
    wait_photo = State()  # Matn ajratish uchun rasm kutish holati
    wait_pdf = State()    # PDF kutish holati
    wait_check = State()  # To'lov chekini kutish holati