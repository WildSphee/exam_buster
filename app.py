import logging
import csv
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the bot token from environment variable
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

CSV_FILE = 'user_data.csv'

def log_interaction(user, user_message, bot_response):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            # Write the header if the file does not exist
            writer.writerow(['user_id', 'username', 'first_name', 'last_name', 'user_message', 'bot_response'])
        writer.writerow([user.id, user.username, user.first_name, user.last_name, user_message, bot_response])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued and log user info."""
    user = update.message.from_user
    user_message = update.message.text
    bot_response = 'Hi!'
    log_interaction(user, user_message, bot_response)
    await update.message.reply_text(bot_response)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued and log user info."""
    user = update.message.from_user
    user_message = update.message.text
    bot_response = 'Help!'
    log_interaction(user, user_message, bot_response)
    await update.message.reply_text(bot_response)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message and log user info."""
    user = update.message.from_user
    user_message = update.message.text
    bot_response = update.message.text
    log_interaction(user, user_message, bot_response)
    await update.message.reply_text(bot_response)

def main() -> None:
    """Start the bot."""
    if TOKEN is None:
        logger.error("No token found. Please set TELEGRAM_BOT_TOKEN in your .env file.")
        return

    application = ApplicationBuilder().token(TOKEN).build()

    # add commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()

if __name__ == '__main__':
    main()