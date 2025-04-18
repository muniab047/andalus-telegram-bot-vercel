import json
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters,CallbackQueryHandler,Application
)
from typing import Dict, Any

from andalus import DB_URI, TOKEN, button_click, button_handler, start
from core.handlers import TelegramHandlers
from core.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from infrastructure.postgres import PostgresPersistence
from core.query import QueryHandler
from core.states.states import BotState
from core.states.transition import BotStateMachine

app = FastAPI()
config = Config()
bot_state = BotState()
bot_state_machine = BotStateMachine()
query_handler = QueryHandler()




handler = TelegramHandlers(bot_state=bot_state, bot_state_machine=bot_state_machine, query_handler=query_handler, config=config)
# SQLAlchemy session maker
def start_session():
    engine = create_engine(DB_URI, client_encoding="utf8")
    return scoped_session(sessionmaker(bind=engine, autoflush=False))

persistence = PostgresPersistence(session=start_session())


application = Application.builder().token(TOKEN).persistence(persistence).build()

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
    my_chat_member: Optional[dict]
    chat_member: Optional[dict]
    chat_join_request: Optional[dict]
    chat_boost: Optional[dict]
    removed_chat_boost: Optional[dict]



def register_application(application):
    # application.add_handler(CommandHandler("start", handler.start))
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler.message_handler))
    # application.add_handler(CallbackQueryHandler(handler.query_handler))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))
    application.add_handler(CallbackQueryHandler(button_click))


@app.post("/webhook")
async def webhook(webhook_data: Dict[Any, Any]):
    register_application(application)
    try:
        await application.initialize()
        await application.process_update(
            Update.de_json(
                json.loads(json.dumps(webhook_data, default=lambda o: o.__dict__)),
                application.bot,
            )
        )
    finally:
        await application.shutdown()
    

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
