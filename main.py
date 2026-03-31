import asyncio
from concurrent.futures import ThreadPoolExecutor
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from deep_translator import GoogleTranslator
TOKEN = "8715665920:AAFVS6tlWIVrM4UmVQSdn58MdstRL4Om0LE"
bot = Bot(token=TOKEN)
dp = Dispatcher()
executor = ThreadPoolExecutor(max_workers=10)
async def get_translation(text, src, dest):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        executor,
        lambda: GoogleTranslator(source=src, target=dest).translate(text)
    )


@dp.message(Command("start"))
async def start(m: Message):
    await m.answer(
        "**Бот-переводчик запущен!**\n\n"
        "Напиши текст на русском или английском, и я мгновенно его переведу.",
        parse_mode="Markdown",
    )


@dp.message()
async def translate_logic(m: Message):
    if not m.text:
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
            f"**Перевод ({source_lang} ➔ {target_lang}):**\n\n{translated_text}",
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Ошибка при переводе: {e}")
        await m.answer("⚠️ Ошибка связи с сервером перевода. Попробуй еще раз через секунду.")
async def main():
    print("--- Бот запущен и работает в ускоренном режиме ---")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")