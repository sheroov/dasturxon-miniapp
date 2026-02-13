import os
import json
import asyncio
from pathlib import Path
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# ===== Загружаем .env =====
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL")

print("WEBAPP_URL =", WEBAPP_URL)

# ===== Создаем бота =====
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ===== Кнопка Mini App =====
def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text="🍱 Menyu (Mini App)",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )]
        ],
        resize_keyboard=True
    )

# ===== Команда /start =====
@dp.message(F.text == "/start")
async def start(message: Message):
    await message.answer(
        "Assalomu alaykum 👋\nMenyuni ochish uchun pastdagi tugmani bosing.",
        reply_markup=main_keyboard()
    )

# ===== Получение данных из Mini App =====
@dp.message(F.web_app_data)
async def webapp_data_handler(message: Message):
    try:
        data = json.loads(message.web_app_data.data)
    except Exception:
        await message.answer("❌ Buyurtma ma'lumotini o‘qib bo‘lmadi.")
        return

    items = data.get("items", [])
    total = data.get("total", 0)
    address = data.get("address", "")
    phone = data.get("phone", "")
    comment = data.get("comment", "")

    text = ["✅ Yangi buyurtma:"]

    for item in items:
        text.append(
            f"• {item['title']} x{item['qty']} = {item['qty'] * item['price']:,} so'm"
        )

    text.append(f"\n💰 Jami: {total:,} so'm")

    if phone:
        text.append(f"📞 Telefon: {phone}")

    if address:
        text.append(f"📍 Manzil: {address}")

    if comment:
        text.append(f"📝 Izoh: {comment}")

    await message.answer("\n".join(text))
    await message.answer("✅ Buyurtma qabul qilindi!", reply_markup=main_keyboard())

# ===== Запуск =====
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

