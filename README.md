# Telegram AI Chat Bot

This project implements a simple Telegram bot that forwards messages to the OpenRouter AI API and returns the response.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file based on `.env.example` and fill in your tokens:
   ```
   BOT_TOKEN=...
   OPENROUTER_API_KEY=...
   BOT_USERNAME=...
   ```
3. Run the bot:
   ```bash
   python main.py
   ```

The bot will start polling for messages. Send a text message to your bot in Telegram to receive a reply from the AI service.