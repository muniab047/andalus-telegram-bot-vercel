from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext

from core.config import Config
from core.query import QueryHandler
from core.states.states import BotState
from core.states.transition import BotStateMachine


class TelegramHandlers:
    def __init__(self, bot_state : BotState, bot_state_machine : BotStateMachine, query_handler : QueryHandler, config : Config):
        self.bot_state = bot_state
        self.bot_state_machine = bot_state_machine
        self.query = query_handler
        self.config = config
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("welcome to andalus")
        
        await self.show_main_menu(update, context)
    
    async def show_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        buttons = [
            [KeyboardButton("Weekly Schedule 🗓️"), KeyboardButton("Availability 🕰️")],
            [KeyboardButton('Student 👨‍🎓'), KeyboardButton('Course Material 📚')],
            [KeyboardButton('Report 📝'), KeyboardButton('Contribution 🙌')]
        ]
        reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        await update.message.reply_text("Main menu", reply_markup=reply_markup)
        context.user_data['state']= self.bot_state.START

    async def select_language(self, update,context, state):
        buttons=[[KeyboardButton("Amharic"),KeyboardButton("Afaan Oromoo")],
                [KeyboardButton("⬅️ Back")]]
        reply_markup= ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        context.user_data['state']= state
        await update.message.reply_text("Select the Language",reply_markup=reply_markup )

    async def select_format (self, update,context, state):
        buttons=[[KeyboardButton("📄 PDF"),KeyboardButton("📱 Mobile App")],
                [KeyboardButton("⬅️ Back")]]
        reply_markup= ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        context.user_data['state']= state
        
        await update.message.reply_text("Select the Format",reply_markup=reply_markup )

    async def check_membership(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id

        try:
            member = await context.bot.get_chat_member(chat_id= self.config.GROUP_CHAT_ID, user_id=user_id)
            if member.status in ['member', 'creator', 'administrator']:
                return True
            else:
                return False
        except Exception as e:
            await update.message.reply_text(f"⚠️ Could not verify membership: {e}")



    async def select_catagory(self, update,context, state):
        buttons=[[KeyboardButton("🌿Natural Science"),KeyboardButton("👥Social Science")],
                [KeyboardButton("⬅️ Back")]]
        reply_markup= ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        context.user_data['state']= state
        
        await update.message.reply_text("Select the Catagory",reply_markup=reply_markup )

    async def show_inlinekeyboard(self, update,course, photo ):
     
        keyboard=[
            
            [InlineKeyboardButton("📕Text Book", callback_data= f'{course} text book')],
            #[InlineKeyboardButton("📖Reference", callback_data= f'{course} reference')],
            [InlineKeyboardButton("👩‍🏫Teachers Guide", callback_data= f'{course} teachers guide')],
            #[InlineKeyboardButton("📝🧠Question", callback_data= f'{course} question')],
            

        ]
        reply_markup= InlineKeyboardMarkup(keyboard)
        await update.message.reply_photo(photo= photo, reply_markup=reply_markup)

    async def handle_availability_selection(self, update, context, text):
        member = await self.check_membership(update, context)

        if not member:
            await update.message.reply_text("⚠️ You need to be a member of the group to access this feature.")
            return
        

        day=update.message.date.strftime('%A')

        if day!= 'Friday' and day!='Saturday':
            if text== 'Throughout the day' or text== 'During my shift only' or text== 'Outside of my shift only' or text=='Not at all':
                context.user_data['availability']=text
                await update.message.reply_text('Specify which courses your student should focus on this week\n Please write all only in one message')
                context.user_data['state']= 'course schedule'
                

            elif text=="I can compromise only if it is necessary by..." or text== 'Other':
                await update.message.reply_text("Tell us what's in your mind")              
                context.user_data['state']= 'necessary'
        else:
           await update.message.reply_text("absent time out")
           await update.message.reply_text('Specify which courses your student should focus on this week\n Please write all only in one message')
           context.user_data['state']= 'course schedule'
        

    
    async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        state = context.user_data.get('state', "original state")
        text = update.message.text
        transition = self.bot_state_machine.get_transition(state, text)

        if state == self.bot_state.START and (text == "Student 👨‍🎓" or text == "Availability 🕰️" or text == "Report 📝") :
            member = await self.check_membership(update, context)

            if not member:
                await update.message.reply_text("⚠️ You need to be a member of andalus members group to access this feature.")
                return


        if text== '🏠 Home':
            await self.show_main_menu(update, context)
            

        elif state == self.bot_state.AWAITING_NECESSARY:
            context.user_data['availability']=text
            await update.message.reply_text('Specify which courses your student should focus on this week\n Please write all only in one message')
            context.user_data['state']= 'course schedule'
        elif state == self.bot_state.AWAITING_COURSE_SCHEDULE:
            message = update.effective_chat
            info =f"Usernmae:@{message.username}\nName:{message.full_name}\nAvailability:{context.user_data.get('availability')}\ncourses of my student:{text}"                      
            await context.bot.send_message(chat_id= self.config.CHAT_ID , text=info)
            await update.message.reply_text(f'{info}\n\n\n Message sent to Academics. Thank you')
            await self.show_main_menu(update, context)



        

        elif transition.reply_markup:
            buttons = transition.reply_markup
            await self.show_keyboard_button(update, context, buttons, transition.next_state, transition.reply_text)
        
        
        elif transition.handler:
            handler = transition.handler
            if handler == "original_button":
                await self.show_main_menu(update, context)
            elif handler == "select_language":
                next_state = transition.next_state
                await self.select_language(update, context, next_state)
            elif handler == "send_document":
                document_url = transition.reply_text
                try:
                    await update.message.reply_document(document= document_url)
                except:
                    await update.message.reply_document(document=f"{document_url}?single")
            elif handler == "select_format":
                next_state = transition.next_state
                await self.select_format(update, context, next_state)
            elif handler == "select_category":
                next_state = transition.next_state
                await self.select_catagory(update, context, next_state)
            elif handler == "show_inlinekeyboard":
                await self.show_inlinekeyboard(update, transition.course, transition.photo)
            elif handler == "handle_availability_selection":
                await self.handle_availability_selection(update, context, text)
        elif transition.next_state:
            context.user_data['state'] = transition.next_state
            if transition.reply_text:
                await update.message.reply_text(transition.reply_text)

        elif transition.reply_text:
            await update.message.reply_text(transition.reply_text)
    async def query_handler (self, update: Update, context :CallbackContext):
        query= update.callback_query
        button_clicked=query.data
        user_name='https://t.me/ethiopian_text_book'
        chat_id=query.message.chat_id
       

        id = await self.query.get_id(button_clicked)
        await self.retrive_data(id, user_name, chat_id, button_clicked)


    async def retrive_data(self, id, user_name, chat_id, file_name):
     
    
        if id:
            await self.config.BOT.send_message(chat_id=chat_id, text= f'here are {file_name}')
        else:
            await self.config.BOT.send_message(chat_id=chat_id, text= f'coming soon')
            
        
        for i in id:
                file_path = f'{user_name}/{i}'
                

                try:
                    await self.config.BOT.send_document(chat_id=chat_id, document=file_path)
                except:
                    try:
                        await self.config.BOT.send_photo(chat_id=chat_id, photo=file_path)
                    except:
                        try:
                            await self.config.BOT.send_document(chat_id=chat_id, document= f'{file_path}?single')
                        except:
                            await self.config.BOT.send_photo(chat_id=chat_id, document= f'{file_path}?single')
            
        


            




        




        
   
    async def show_keyboard_button(self, update, context,courses, states, message):
        buttons=[]
        for course in courses:        
            buttons.append([KeyboardButton(course)])

        buttons.append([KeyboardButton("🏠 Home"),KeyboardButton("⬅️ Back")])

        reply_markup= ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        await update.message.reply_text(message, reply_markup=reply_markup)
        context.user_data['state']= states


    