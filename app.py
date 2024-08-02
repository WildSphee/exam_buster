import logging
import os
import pandas as pd
from dotenv import load_dotenv
from telegram import Update, User
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from chatbots.openai import call_openai

# Load environment variables from .env file
load_dotenv()

# Get the bot token from environment variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

CSV_FILE = "user_data.csv"


def log_interaction(user: User, user_message: str, bot_response: str) -> None:
    df_new = pd.DataFrame(
        [
            {
                "user_id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "user_message": user_message,
                "bot_response": bot_response,
            }
        ]
    )

    # Append the new interaction to the existing CSV file
    if os.path.isfile(CSV_FILE):
        df_new.to_csv(CSV_FILE, mode="a", header=False, index=False)
    else:
        df_new.to_csv(CSV_FILE, mode="w", header=True, index=False)


def get_chat_history(user_id: int) -> list[dict[str, str]]:
    if not os.path.isfile(CSV_FILE):
        return []

    df = pd.read_csv(CSV_FILE)
    user_history = df[df['user_id'] == user_id]

    formatted_history = []
    for _, row in user_history.iterrows():
        if pd.notna(row['bot_response']):  # Check if bot_response is not NaN
            formatted_history.append({"role": "assistant", "content": row['bot_response']})
        formatted_history.append({"role": "user", "content": row['user_message']})

    return formatted_history


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued and log user info."""
    user: User = update.message.from_user
    user_message: str = update.message.text
    bot_response: str = "To start, simply type anything~"
    log_interaction(user, user_message, bot_response)
    await update.message.reply_text(bot_response)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued and log user info."""
    user: User = update.message.from_user
    user_message: str = update.message.text
    bot_response: str = "This is a simple telegram chatbot, type anything to start!"
    log_interaction(user, user_message, bot_response)
    await update.message.reply_text(bot_response)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message and log user info."""
    user: User = update.message.from_user
    user_message: str = update.message.text

    chat_history = get_chat_history(user.id)
    chat_history.append({"role": "user", "content": user_message})
    bot_response: str = call_openai(chat_history)

    log_interaction(user, user_message, bot_response)
    await update.message.reply_text(bot_response)


def main() -> None:
    """Start the bot."""
    if TOKEN is None:
        logger.error("No token found. Please set TELEGRAM_BOT_TOKEN in your .env file.")
        return

    application = ApplicationBuilder().token(TOKEN).build()

    # Add commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()


if __name__ == "__main__":
    main()