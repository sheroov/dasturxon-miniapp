import os
import json
import asyncio
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

load_dotenv()

BOT_TOKEN = os.getenv("8050351233:AAGBc74-GxtfJFBiv89NBMEZC9Cv0_Zyqpo")
WEBAPP_URL = os.getenv("https://track.wolt.com/s/CFqQR43bV6Mvz3zBqaCyig")  # https ссылка на мини-апп

bot = Bot(token="8050351233:AAGBc74-GxtfJFBiv89NBMEZC9Cv0_Zyqpo")
dp = Dispatcher()

def kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🍱 Menyu (Mini App)", web_app=WebAppInfo(url=WEBAPP_URL))]
        ],
        resize_keyboard=True
    )

@dp.message(F.text == "/start")
async def start(message: Message):
    await message.answer("🍱 Menyu mini-ilova orqali ochiladi 👇", reply_markup=kb())

@dp.message(F.web_app_data)
async def webapp_data(message: Message):
    try:
        data = json.loads(message.web_app_data.data)
    except Exception:
        await message.answer("❌ Xatolik: buyurtma ma'lumoti noto'g'ri.")
        return

    items = data.get("items", [])
    total = data.get("total", 0)
    address = data.get("address", "").strip()
    phone = data.get("phone", "").strip()
    comment = data.get("comment", "").strip()

    if not items:
        await message.answer("🛒 Savat bo‘sh.")
        return

    lines = ["✅ Yangi buyurtma:"]
    for it in items:
        lines.append(f"• {it['title']} x{it['qty']} = {it['qty']*it['price']:,} so'm")

    lines.append(f"\n💰 Jami: {total:,} so'm")
    if phone:
        lines.append(f"📞 Tel: {phone}")
    if address:
        lines.append(f"📍 Manzil: {address}")
    if comment:
        lines.append(f"📝 Izoh: {comment}")

    await message.answer("\n".join(lines))
    await message.answer("✅ Buyurtma qabul qilindi! Tez orada bog‘lanamiz.", reply_markup=kb())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

