# TELEGRAM EXAM BOT, this bot saves no history and made for answering PMP exam only, cuz the author didn't study for it

import os

from dotenv import load_dotenv
from telegram import Update, User
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# from db import DB
from llms.openai import call_openai
from llms.prompt import EXAM_BOT_PROMPT

load_dotenv()

TOKEN = os.getenv("TELEGRAM_EXAM_BOT_TOKEN")


async def start_command(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued and log user info. also clears context"""
    bot_response: str = "ready for exams:"

    await update.message.reply_text(bot_response)


async def echo(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message and log user info."""
    user: User = update.message.from_user
    user_message: str = update.message.text

    bot_response: str = call_openai([], user, user_message, EXAM_BOT_PROMPT)

    await update.message.reply_text(bot_response)


def main() -> None:
    """Start the bot."""
    if TOKEN is None:
        print("No token found. Please set TELEGRAM_EXAM_BOT_TOKEN in your .env file.")
        return

    application = ApplicationBuilder().token(TOKEN).build()

    # Add commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()


if __name__ == "__main__":
    main()
