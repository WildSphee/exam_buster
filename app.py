import logging
import os

from dotenv import load_dotenv
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update, User
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from chatbots.openai import call_openai
from db import _clear_chat_history, _get_chat_history, _log_interaction

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

keyboard = [[KeyboardButton("/clear")]]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def help_command(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued and log user info."""
    user_message: str = update.message.text
    bot_response: str = "This is a simple telegram chatbot, type anything to start! /clear to clear context!"

    user: User = update.message.from_user
    _log_interaction(user, user_message, bot_response)
    await update.message.reply_text(bot_response)


async def clear_command(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Clear the username in the chat history."""
    user_message: str = update.message.text
    bot_response: str = "Context cleared"
    user: User = update.message.from_user
    _log_interaction(user, user_message, bot_response)
    _clear_chat_history(user)

    await update.message.reply_text(bot_response)


async def echo(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message and log user info."""
    user: User = update.message.from_user
    user_message: str = update.message.text

    chat_history = _get_chat_history(str(user.id))
    chat_history.append({"role": "user", "content": user_message})
    bot_response: str = call_openai(chat_history, user)

    _log_interaction(user, user_message, bot_response)
    await update.message.reply_text(bot_response, reply_markup=reply_markup)


def main() -> None:
    """Start the bot."""
    if TOKEN is None:
        logger.error("No token found. Please set TELEGRAM_BOT_TOKEN in your .env file.")
        return

    application = ApplicationBuilder().token(TOKEN).build()

    # Add commands
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("clear", clear_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()


if __name__ == "__main__":
    main()
