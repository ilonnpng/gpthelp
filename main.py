import os
import aiohttp
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters


# Загружаем токены из .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
BOT_USERNAME = os.getenv("BOT_USERNAME")


# Асинхронная функция для общения с OpenRouter
async def ask_ai(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": f"https://t.me/{BOT_USERNAME}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",
        "messages": [
            {"role": "system", "content": "Ты — дружелюбный ассистент, всегда отвечай только на русском языке, даже если спрашивают на английском или другом языке."},
            {"role": "user", "content": prompt}
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
        ) as response:
            response.raise_for_status()
            json_response = await response.json()
    return json_response["choices"][0]["message"]["content"]


# Обработчик сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.chat.send_action(action="typing")
        user_message = update.message.text
        reply = await ask_ai(user_message)
    except Exception as e:
        reply = f"Извините, сервис временно недоступен.\n{e}"
    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
