import logging
import os
import pandas as pd
from pydantic import BaseModel, Field
from typing import Optional
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv


class Interaction(BaseModel):
    user_id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    user_message: str
    bot_response: str
