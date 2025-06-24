import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.executor import start_webhook
from dotenv import load_dotenv

from data.hangeul import hangeul_letters_data
from data.grammar import grammar_1A, grammar_1B

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
PREMIUM_GROUP_LINK = os.getenv("PREMIUM_LINK")
TOPIK_LINK = os.getenv("TOPIK_LINK")

WEBHOOK_HOST = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 8000))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(
    KeyboardButton("📚 TOPIK 1"),
    KeyboardButton("📖 서울대 한국어 1A/1B"),
    KeyboardButton("☀️ Harflar"),
    KeyboardButton("💎 Premium darslar")
)

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer(
        "Assalomu alaykum!\nKoreys tili o‘rgatadigan botga xush kelibsiz.\nQuyidagi menydan foydalaning:",
        reply_markup=main_menu
    )

# === Harflar ===
@dp.message_handler(lambda message: message.text == "☀️ Harflar")
async def show_letter_menu(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=4)
    for harf in hangeul_letters_data.keys():
        markup.insert(InlineKeyboardButton(harf, callback_data=f"harf_{harf}"))
    markup.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main"))
    await message.answer("Quyidagi harflardan birini tanlang:", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data.startswith("harf_"))
async def show_letter_info(callback: types.CallbackQuery):
    harf = callback.data.replace("harf_", "")
    matn = hangeul_letters_data.get(harf, "Ma’lumot topilmadi")
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_letters"))
    await callback.message.edit_text(f"☀️ {harf}\n{matn}", reply_markup=markup)
    await callback.answer()

@dp.callback_query_handler(lambda c: c.data == "back_to_letters")
async def back_to_letters(callback: types.CallbackQuery):
    markup = InlineKeyboardMarkup(row_width=4)
    for harf in hangeul_letters_data.keys():
        markup.insert(InlineKeyboardButton(harf, callback_data=f"harf_{harf}"))
    markup.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main"))
    await callback.message.edit_text("Quyidagi harflardan birini tanlang:", reply_markup=markup)
    await callback.answer()

# === Grammatikalar ===
@dp.message_handler(lambda message: message.text == "📖 서울대 한국어 1A/1B")
async def show_books(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("1A 📚", callback_data="book_1A"),
        InlineKeyboardButton("1B 📖", callback_data="book_1B"),
        InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main")
    )
    await message.answer("Qaysi kitobni tanlaysiz?", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == "book_1A")
async def show_1a_menu(callback: types.CallbackQuery):
    markup = InlineKeyboardMarkup(row_width=1)
    for key in grammar_1A:
        markup.add(InlineKeyboardButton(key, callback_data=key))
    markup.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="show_books_menu"))
    await callback.message.edit_text("1A grammatikalaridan birini tanlang:", reply_markup=markup)
    await callback.answer()

@dp.callback_query_handler(lambda c: c.data == "book_1B")
async def show_1b_menu(callback: types.CallbackQuery):
    markup = InlineKeyboardMarkup(row_width=1)
    for key in grammar_1B:
        markup.add(InlineKeyboardButton(key, callback_data=key))
    markup.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="show_books_menu"))
    await callback.message.edit_text("1B grammatikalaridan birini tanlang:", reply_markup=markup)
    await callback.answer()

@dp.callback_query_handler(lambda c: c.data == "show_books_menu")
async def show_books_menu(callback: types.CallbackQuery):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("1A 📚", callback_data="book_1A"),
        InlineKeyboardButton("1B 📖", callback_data="book_1B"),
        InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main")
    )
    await callback.message.edit_text("Qaysi kitobni tanlaysiz?", reply_markup=markup)
    await callback.answer()

@dp.callback_query_handler(lambda c: c.data in grammar_1A)
async def show_1a_grammar(callback: types.CallbackQuery):
    key = callback.data
    text = grammar_1A.get(key, "Ma'lumot topilmadi")
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Orqaga", callback_data="book_1A"))
    await callback.message.edit_text(f"📘 {text}", reply_markup=markup)
    await callback.answer()

@dp.callback_query_handler(lambda c: c.data in grammar_1B)
async def show_1b_grammar(callback: types.CallbackQuery):
    key = callback.data
    text = grammar_1B.get(key, "Ma'lumot topilmadi")
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Orqaga", callback_data="book_1B"))
    await callback.message.edit_text(f"📗 {text}", reply_markup=markup)
    await callback.answer()

# === TOPIK 1 ===
@dp.message_handler(lambda message: message.text == "📚 TOPIK 1")
async def topik_handler(message: types.Message):
    await message.reply(
        f"📚 TOPIK 1 darslariga hush kelibsiz!\nUlanish uchun link: {TOPIK_LINK}",
        disable_web_page_preview=True
    )

# === Premium ===
@dp.message_handler(lambda message: message.text == "💎 Premium darslar")
async def premium_info(message: types.Message):
    text = (
        "💎 PREMIUM DARS TARIFI\n\n"
        "📌 Imkoniyatlar:\n"
        "🔹 Har ikki kunda jonli dars\n"
        "🔹 Faqat premiumlar uchun yopiq materiallar\n"
        "🔹 So‘z boyligi, Kareys tili 0dan o‘rganish\n"
        "🔹 Savol-javoblar uchun yopiq guruh\n\n"
        "💰 Narxi: 30 000 so‘m (oyiga)\n"
        "💳 To‘lov uchun karta: 5614 6818 1030 9850\n\n"
        "📅 To‘lov cheki surati bilan birga 'PREMIUM' deb yozing!"
    )
    await message.answer(text)

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_check(message: types.Message):
    if "premium" in message.caption.lower():
        await bot.send_message(ADMIN_ID, f"💳 Yangi premium foydalanuvchi:\n👤 {message.from_user.full_name}\n🆔 {message.from_user.id}")
        await bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=message.caption)
        await message.reply(f"✅ Chek qabul qilindi!\nSizga link: {PREMIUM_GROUP_LINK}")
    else:
        await message.reply("❗ Iltimos, captionda 'PREMIUM' deb yozing.")

# === Orqaga ===
@dp.callback_query_handler(lambda c: c.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, "⬅️ Asosiy menyu:", reply_markup=main_menu)
    await callback.message.delete()
    await callback.answer()

# === Webhook start ===
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    print("✅ Webhook o‘rnatildi:", WEBHOOK_URL)

async def on_shutdown(dp):
# await bot.delete_webhook()
    print("❌ Webhook o‘chirildi")

if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
