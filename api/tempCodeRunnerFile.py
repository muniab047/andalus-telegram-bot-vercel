def main():
 
    updater = Updater(Bot(Token),Queue(maxsize=0) )
    #dp = updater.dispatcher
    app= Application.builder().token(Token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))
    app.add_handler(CallbackQueryHandler(button_click))


    #updater.start_polling()
    app.run_polling()
    app.idle()
    schedule_messages()

    
    

    while True:
        schedule.run_pending()
        time.sleep(1)
