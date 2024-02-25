import json
import os
from typing import Optional

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters,CallbackQueryHandler,Application
)

from andalus import start, button_handler, button_click

dotenv_path = find_dotenv()
load_dotenv()
TOKEN = os.getenv("TOKEN")

app = FastAPI()
chat_users = {}

application = Application.builder().token(TOKEN).build()


class TelegramWebhook(BaseModel):
    update_id: int
    message: Optional[dict]
    edited_message: Optional[dict]
    channel_post: Optional[dict]
    edited_channel_post: Optional[dict]
    inline_query: Optional[dict]
    chosen_inline_result: Optional[dict]
    callback_query: Optional[dict]
    shipping_query: Optional[dict]
    pre_checkout_query: Optional[dict]
    poll: Optional[dict]
    poll_answer: Optional[dict]



def register_application(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))
    application.add_handler(CallbackQueryHandler(button_click))


@app.post("/webhook")
async def webhook(webhook_data: TelegramWebhook):
    register_application(application)
    await application.initialize()
    await application.process_update(
        Update.de_json(
            json.loads(json.dumps(webhook_data.dict(), default=lambda o: o.__dict__)),
            application.bot,
        )
    )

    # bot = Bot(token=TOKEN)

    # update = Update.de_json(webhook_data.__dict__, bot)

    # await botApp.initialize()
    # await botApp.start()
    # await botApp.process_update(update)
    # await botApp.updater.stop()
    # await botApp.stop()

    return {"message": "ok"}


@app.get("/")
def index():
    return {"message": "Hello World"}