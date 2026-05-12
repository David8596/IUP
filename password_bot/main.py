from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
import asyncio
from generator import gen_pass
from validator import check_pass

from config import BOT_TOKEN
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

last_paswd = {}

@dp.message(Command("start"))
async def start_cmd(message: Message):
    text = """Я бот для работы с паролями.

Что я умею:
/generate - создать пароль
/check пароль - проверить надёжность пароля
"""
    await message.answer(text)

@dp.message(Command("generate"))
async def gen_cmd(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Лёгкий", callback_data="easy")],
        [InlineKeyboardButton(text="Средний", callback_data="medium")],
        [InlineKeyboardButton(text="Сложный", callback_data="hard")],
    ])
    await message.answer("Выбери сложность:", reply_markup=keyboard)

@dp.callback_query(F.data == "easy")
async def easy_gen(callback: CallbackQuery):
    paswd = gen_pass(length=8, letters=True, digits=False, special=False)
    await show_res(callback, paswd)

@dp.callback_query(F.data == "medium")
async def medium_gen(callback: CallbackQuery):
    paswd = gen_pass(length=10, letters=True, digits=True, special=False)
    await show_res(callback, paswd)

@dp.callback_query(F.data == "hard")
async def hard_gen(callback: CallbackQuery):
    paswd = gen_pass(length=12, letters=True, digits=True, special=True)
    await show_res(callback, paswd)

async def show_res(callback: CallbackQuery, paswd: str):
    last_paswd[callback.from_user.id] = paswd
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Создать ещё", callback_data="again")],
    ])
    await callback.message.answer(f"Пароль: {paswd}", reply_markup=keyboard)

@dp.callback_query(F.data == "again")
async def again_gen(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Лёгкий", callback_data="easy")],
        [InlineKeyboardButton(text="Средний", callback_data="medium")],
        [InlineKeyboardButton(text="Сложный", callback_data="hard")],
    ])
    await callback.message.edit_text("Выбери сложность:", reply_markup=keyboard)

@dp.message(Command("check"))
async def check_cmd(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Отправь так: /check твойпароль123")
        return
    
    paswd = args[1]
    score, advice = check_pass(paswd)
    stars = "*" * score + "x" * (5 - score)
    await message.answer(f"Оценка: {stars} ({score}/5)\n\n{advice}")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
