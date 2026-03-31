import asyncio
from concurrent.futures import ThreadPoolExecutor
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession
from deep_translator import GoogleTranslator

proxy_url = "http://proxy.server:3128"
session = AiohttpSession(proxy=proxy_url)
TOKEN = "8715665920:AAHBUGeArVjcjJ6m5i8lH36vwpTG61C2KMg"

bot = Bot(token=TOKEN, session=session)
dp = Dispatcher()
executor = ThreadPoolExecutor(max_workers=10)
BAD_WORDS = ["плохоеслово1", "плохоеслово2"]

def contains_bad_words(text):
    text_lower = text.lower()
    for word in BAD_WORDS:
        if word in text_lower:
            return True
    return False

async def get_translation(text, src, dest):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        executor,
        lambda: GoogleTranslator(source=src, target=dest).translate(text)
    )

@dp.message(Command("start"))
async def start(m: Message):
    await m.answer(
        "**Fast Translator Bot is ready!**\n\n"
        "Send me any text in English or Russian, and I will translate it instantly.\n"
        "*(Note: Profanity is filtered)*",
        parse_mode="Markdown"
    )

@dp.message()
async def translate_logic(m: Message):
    if not m.text:
        return
    if contains_bad_words(m.text):
        await m.answer("Sorry, I don't translate messages containing profanity.")
        return
    russian_chars = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    if any(char in russian_chars for char in m.text.lower()):
        source_lang, target_lang = 'ru', 'en'
    else:
        source_lang, target_lang = 'en', 'ru'
    await bot.send_chat_action(m.chat.id, "typing")
    try:
        translated_text = await get_translation(m.text, source_lang, target_lang)
        await m.answer(
            f" **Translation ({source_lang} ➔ {target_lang}):**\n\n{translated_text}",
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Error: {e}")
        await m.answer(" Connection error. Please try again in a few seconds.")

async def main():
    print("--- Бот запущен через PROXY на PythonAnywhere ---")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped")
# that's my telegram bot t.me/LearnEnglishGGBot