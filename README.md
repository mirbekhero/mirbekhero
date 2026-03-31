A professional, high-speed Telegram translator bot built with **aiogram 3.x**. The bot automatically detects the input language and provides instant translations, ensuring a smooth user experience through multi-threading.
Key Features
* **Auto Language Detection**: Automatically recognizes whether you are typing in Russian or English and translates accordingly (RU ➔ EN / EN ➔ RU).
* **High Performance**: Uses `ThreadPoolExecutor` to handle translation requests asynchronously. The bot never "freezes" while waiting for a response from translation servers.
* **Profanity Filter**: Includes a built-in content filter. The bot will politely refuse to translate messages containing offensive language or slurs.
* **Real-time Feedback**: Sends a "typing..." chat action immediately, so users know the bot is processing their request.
Tech Stack
* **Language**: Python 3.10+
* **Framework**: `aiogram 3.x` (Asyncio)
* **Translation Engine**: `deep-translator` (Google Translate API)
* **Parallelism**: `concurrent.futures.ThreadPoolExecutor`
