import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession
from deep_translator import GoogleTranslator
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
def get_bot_instance():
    if "home" in os.getcwd():
        proxy_url = "http://proxy.server:3128"
        session = AiohttpSession(proxy=proxy_url)
        print("Запуск на сервере через PROXY")
        return Bot(token=TOKEN, session=session)
    else:
        print("💻 Запуск на локальном ПК (напрямую)")
        return Bot(token=TOKEN)
bot = get_bot_instance()
dp = Dispatcher()
executor = ThreadPoolExecutor(max_workers=10)
BAD_WORDS = ["плохоеслово1", "плохоеслово2"]
def contains_bad_words(text):
    text_lower = text.lower()
    return any(word in text_lower for word in BAD_WORDS)
async def get_translation(text, src, dest):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        executor,
        lambda: GoogleTranslator(source=src, target=dest).translate(text)
    )
@dp.message(Command("start"))
async def start(m: Message):
    await m.answer(
        "👋 **Hello! I am your secure translator bot.**\n\n"
        "I use a hidden token and automatic environment detection.",
        parse_mode="Markdown"
    )
@dp.message()
async def translate_logic(m: Message):
    if not m.text:
        return
    if contains_bad_words(m.text):
        await m.answer("⚠️ Profanity detected. Translation denied.")
        return
    russian_chars = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    is_russian = any(char in russian_chars for char in m.text.lower())
    source_lang, target_lang = ('ru', 'en') if is_russian else ('en', 'ru')
    await bot.send_chat_action(m.chat.id, "typing")

    try:
        translated_text = await get_translation(m.text, source_lang, target_lang)
        await m.answer(f"🌍 **{source_lang.upper()} ➔ {target_lang.upper()}:**\n\n{translated_text}", parse_mode="Markdown")
    except Exception as e:
        await m.answer("⚠️ Translation error. Server might be busy.")
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())
# that's my telegram bot t.me/LearnEnglishGGBot