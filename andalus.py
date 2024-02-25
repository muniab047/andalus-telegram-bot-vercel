import logging
import schedule
from telegram.ext import  CommandHandler, MessageHandler, filters,CallbackContext,CallbackQueryHandler,Application, Updater
from telegram import KeyboardButton, ReplyKeyboardMarkup,Update, InlineKeyboardButton, InlineKeyboardMarkup,Bot
from asyncio import Queue
import time
import os
from dotenv import load_dotenv
from mongopersistence import MongoPersistence

load_dotenv()

TOKEN = os.getenv("TOKEN")
MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

logging.basicConfig(level=logging.INFO)
STUDENTS=['Abas', 'Abdulkadir','Amar','Asiya','Ferhan', 'Hanan','Haniya', 'Hilal', 'Rahmet 06', 'Rahmet (Rim)','Muaz','Mubarek', 'Musab', 'Rahmet 05','Sehmi','Seid','Sekina','Sifen', 'Yezid' ]

TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)
#app = Application.builder().token(Token).build()

persistence = MongoPersistence(
        mongo_url=MONGO_URL,
        db_name=DB_NAME,
        name_col_user_data="user-data",  # optional
        name_col_chat_data="chat-data",  # optional
        name_col_bot_data="bot-data",  # optional
        name_col_conversations_data="conversations",  # optional
        create_col_if_not_exist=True,  # optional
        load_on_flush=False,
        update_interval=5
    )

async def original_button(update, context):
    buttons=[
        [KeyboardButton("Weekly Schedule 🗓️"), KeyboardButton("Availability 🕰️")],
        [KeyboardButton('Student 👨‍🎓'), KeyboardButton('Course Material 📚')],
        [KeyboardButton('Report 📝'), KeyboardButton('Contribution 🙌')]
    ]

    reply_markup =ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text("welcome to andalus", reply_markup=reply_markup)
    context.user_data['state']= 'original state'


async def start(update, context ):
    await original_button(update,context)



async def send_message(update, context, message):
    await context.bot.send_message(chat_id=6376132913, text=message)


async def show_keyboard_button(update, context, courses, states, message):
    buttons=[]
    for course in courses:        
        buttons.append([KeyboardButton(course)])

    buttons.append([KeyboardButton("🏠 Home"),KeyboardButton("⬅️ Back")])

    reply_markup= ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text(message, reply_markup=reply_markup)
    context.user_data['state']= states
    await persistence.update_user_data(update.effective_user.id, context.user_data)


async def select_language(update,context, state):
    buttons=[[KeyboardButton("Amharic"),KeyboardButton("Afaan Oromoo")],
             [KeyboardButton("⬅️ Back")]]
    reply_markup= ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    context.user_data['state']= state
    await persistence.update_user_data(update.effective_user.id, context.user_data)
    await update.message.reply_text("Select the Language",reply_markup=reply_markup )


async def select_catagory(update,context, state):
    buttons=[[KeyboardButton("🌿Natural Science"),KeyboardButton("👥Social Science")],
             [KeyboardButton("⬅️ Back")]]
    reply_markup= ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    context.user_data['state']= state
    
    await persistence.update_user_data(update.effective_user.id, context.user_data)
    await update.message.reply_text("Select the Catagory",reply_markup=reply_markup )

async def select_format (update,context, state):
    buttons=[[KeyboardButton("📄 PDF"),KeyboardButton("📱 Mobile App")],
             [KeyboardButton("⬅️ Back")]]
    reply_markup= ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    context.user_data['state']= state
    
    await persistence.update_user_data(update.effective_user.id, context.user_data)
    await update.message.reply_text("Select the Format",reply_markup=reply_markup )


async def show_inlinekeyboard(update,course, photo ):
     
     keyboard=[
        
        [InlineKeyboardButton("📕Text Book", callback_data= f'{course} text book')],
        #[InlineKeyboardButton("📖Reference", callback_data= f'{course} reference')],
        [InlineKeyboardButton("👩‍🏫Teachers Guide", callback_data= f'{course} teachers guide')],
        #[InlineKeyboardButton("📝🧠Question", callback_data= f'{course} question')],
        

    ]
     reply_markup= InlineKeyboardMarkup(keyboard)
     await update.message.reply_photo(photo= photo, reply_markup=reply_markup)
     

async def sunday_message():
    await bot.send_message(chat_id=-1001737401699, text='Aselamualeykum werahmetulahi weberekathu Dear Andalus members,\n\nWe are pleased to inform you that the Availability Selection feature is now active. You can choose your availability until Friday at 00:00.\n\nThank you! ')
async def tuesday_message():
    await bot.send_message(cha_id=-1001737401699, text="Aselamualeykum werahmetulahi weberekathu Dear Andalus members,\n\nFor those who haven't yet selected their availability for this week, please do so before Friday at 00:00. After this deadline, your availability will be set to absent automatically.\n\n Thank you! ")
async def thursday_message():
    await bot.send_message(chat_id=-1001737401699, text='Aselamualeykum werahmetulahi weberekathu Dear Andalus members,\n\nThe Availability Selection period has now ended. If anyone has not yet made their selection, they will be marked as absent. However, we still require the list of courses that students need to study. Please send them as soon as possible.\n\nThank you!')




async def schedule_messages():
    # Define the days you want to send messages
    days_to_send = ['Tuesday', 'Sunday', 'Thursday']

    # Schedule messages for the specified days
    for day in days_to_send:
        schedule.every().sunday.at("12:00").do(sunday_message)
        schedule.every().tuesday.at("12:00").do(tuesday_message)
        schedule.every().thursday.at("00:00").do(thursday_message)







async def retrive_data(query, id, user_name, chat_id, file_name):
     
    
     if id:
         await bot.send_message(chat_id=chat_id, text= f'here are {file_name}')
     else:
         await bot.send_message(chat_id=chat_id, text= f'coming soon')
         
     
     for i in id:
            file_path = f'{user_name}/{i}'
            

            try:
                await bot.send_document(chat_id=chat_id, document=file_path)
            except:
                try:
                    await bot.send_photo(chat_id=chat_id, photo=file_path)
                except:
                    try:
                        await bot.send_document(chat_id=chat_id, document= f'{file_path}?single')
                    except:
                        await bot.send_photo(chat_id=chat_id, document= f'{file_path}?single')
         
     

        
                    



async def button_handler(update:Update,context:CallbackContext):
    state=context.user_data.get('state', 'original state')
    text= update.message.text
    

    if text== '🏠 Home':
        await original_button(update,context)
        

    if state== "original state":
        if text== "Weekly Schedule 🗓️":
            await update.message.reply_text("Click the link \n https://docs.google.com/document/d/1wTghQrSYfeZS6zES7vq4sv42tN-FrCGn9OMdSGr7Jfw/edit?usp=sharing")
        elif text== "Availability 🕰️":
            updatedState= 'availability'
            buttons=['Throughout the day',
                     'During my shift only',
                     'Outside of my shift only',                    
                     'I can compromise only if it is necessary by...',
                     'Not at all',
                     'Other']
            message= "Select your availability for this upcoming Saturday"
            await show_keyboard_button(update,context,buttons,updatedState,message)

        elif text=='Course Material 📚':
            updatedState= 'grade'
            buttons=['👶 KG','Grade 1️⃣','Grade 2️⃣','Grade 3️⃣','Grade 4️⃣','Grade 5️⃣','Grade 6️⃣','Grade 7️⃣','Grade 8️⃣','Grade 9️⃣','Grade 1️⃣0️⃣','Grade 1️⃣1️⃣','Grade 1️⃣2️⃣']
            message ='Select grade'
            await show_keyboard_button(update, context, buttons, updatedState,message)

            

        elif text== 'Student 👨‍🎓':
            updatedState= 'student'
            buttons=['Student information', 'Study schedule']
            message= 'Select your Choice'
            await show_keyboard_button(update, context, buttons,updatedState, message)

        elif text=='Report 📝':
            await update.message.reply_text("Click the link \n This link is only available for amirs and report sector\n\nhttps://drive.google.com/drive/folders/10FVxpAKYKh3m9nn27idvNMivLucA5BfW?usp=sharing")
        elif text=='Contribution 🙌':
            await update.message.reply_text("Click the link \n https://docs.google.com/forms/d/e/1FAIpQLSc_MDD3QDFb1MiQCYhIxW5tSXhJ1Bu9WTi-6k-7eu7Li9hZYg/viewform?usp=sf_link")

    
    elif state=="availability":
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


        if text=="⬅️ Back":
            await original_button(update, context)



    elif state== 'necessary':
        context.user_data['availability']=text
        await update.message.reply_text('Specify which courses your student should focus on this week\n Please write all only in one message')
        context.user_data['state']= 'course schedule'


    elif state=='course schedule':
        message = update.effective_chat
        info =f"Usernmae:@{message.username}\nName:{message.full_name}\nAvailability:{context.user_data.get('availability')}\ncourses of my student:{text}"                      
        await send_message(update, context ,info )
        await update.message.reply_text(f'{info}\n\n\n Message sent to Academics. Thank you')
        context.user_data['state']= 'availability'


    elif state=='student':
        if text== 'Student information':
            updatedState= 'student info'
            message= 'Select your student'
            buttons= STUDENTS
            await show_keyboard_button(update, context, buttons, updatedState, message )

        elif text== 'Study schedule':
            updatedState= 'student schedule'
            message= 'Select your student'
            buttons= STUDENTS
            await show_keyboard_button(update, context, buttons, updatedState, message )

        elif text=='⬅️ Back':
            await original_button(update, context)

    elif state=='student info':
        if text=="Abas":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/document/d/16X1Nugg362hZXLDPHgfiYJc8GivTUuTGfG0icerU7s4/edit?usp=sharing")
        elif text=="Abdulkadir":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/document/d/14xuils39cYc8L14EWZAkLlmj7EaBaI18zu-rtDge_ps/edit?usp=sharing")
        elif text=="Amar":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/document/d/1KO629Ao_NdVyw1WHe0azw-v7jeCjg2vcl6eaFkf9KZs/edit?usp=sharing")
        elif text=="Asiya":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/document/d/1bO6z5UOahtv1bfIsGuqbYYcrqCvOidJmn-j0Ld1IoNI/edit?usp=sharing")
        elif text=="Hanan":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/document/d/1ebj8pAY1sCWAE4nzZTgsu-iwgPmOt1PBDlXtVnxgYWQ/edit?usp=sharing")
        elif text=="Haniya":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/document/d/1dN6ntan1p_ZejgAkz0W33lSf7v-0DyPOiNyKzptuIaw/edit?usp=sharing")
        elif text=="Hilal":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/document/d/1g7_Fsr_4jJPLx0CLc_9WSSr8R5B7cr7zCS3i2Gh__zI/edit?usp=sharing")
        elif text=="Muaz":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/document/d/1xrr9UT8-LyFuFQTf69De_eytPpjRlkkU-Jl00bG9Fbo/edit?usp=sharing")
        elif text=="Mubarek":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/document/d/1zA94W1DExg6KD-2vTFTl2v_bINT2NDpXT0-oeC1otw0/edit?usp=sharing")
        elif text=="Musab":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/document/d/1UsL1S55pqGSu9UGz_jWvVcn1lF86Jud4ZdkOrfjjeiY/edit?usp=sharing")
        elif text=="Rahmet (Rim)":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/document/d/1sxvuWVTqnffM1vE3nLO9uBq71drNI5x7i2TUS5mj5wM/edit?usp=sharing")
        elif text=="Rahmet 05":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/document/d/1zBnroOifBFxbi89jOkkTI0bZKhFuImkE3clwePu9I74/edit?usp=sharing")
        elif text=="Rahmet 06":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/document/d/1mL36Zs-6PQZXYdn3bmigviJzDzlLdIOPEH-9VxOgvFA/edit?usp=sharing")
        elif text=="Ferhan":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/document/d/12JaCMZ4TQUX9ycpL9-9xllmpKE0iR6zPb7bzce_ihvo/edit?usp=sharing")
        elif text=="Sifen":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/document/d/1EBCfoVHFPzXWvv3dQC_hQBmT4G75-_lIalUX0TL7q6M/edit?usp=sharing")
        elif text=="Sehmi":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/document/d/1dwD1omNwZVVaG6ZDTNuo8tw59XY9xOW91Dbx-E2mTR8/edit?usp=sharing")
        elif text=="Seid":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/document/d/1p5RBR-mC5tUtN0wlH-FMJFh5a1z17PTN3Vyd3naJEbQ/edit?usp=sharing")
        elif text=="Sekina":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/document/d/1nk_9KeEbVv7YknuMsjMr_YZT7sMEDzgyZNOjzJ2u63Y/edit?usp=sharing")
        elif text=="Yezid":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/document/d/1h-PMfE2hqqk7vLJ-31_ni65oUyzjRFw0goSejbMcMVM/edit?usp=sharing")
        elif text=='⬅️ Back':
            updatedState= 'student'
            buttons=['Student information', 'Study schedule']
            message= 'Select your Choice'
            await show_keyboard_button(update, context, buttons,updatedState, message)

    

    elif state=='student schedule':
        if text=="Abas":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/spreadsheets/d/1Wr7WNV4oP0OpZiFfo-XXPTBZ1gi_TEBvHNei3YKx558/edit?usp=sharing")
        elif text=="Abdulkadir":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/spreadsheets/d/1lBTneuuUtgVy2CsMNLeeCZ8a9pkTp_B8Pv-s4yMlulk/edit?usp=sharing")
        elif text=="Amar":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/spreadsheets/d/1-n1nuI7rQPHDb0NQ1fYA70oNe-k7W2xgfOTc7EhBbZ4/edit?usp=sharing")
        elif text=="Asiya":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/spreadsheets/d/1B04b-3pqT2ox4171vDv6ViqfgvfKyj5JldlUVUrsN5I/edit?usp=sharing")
        elif text=="Ferhan":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/spreadsheets/d/1R5wrevnoV3f1hP7BZnDF1hstmws8QE1HonC3tyyl5ks/edit?usp=sharing")
        elif text=="Sifen":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/spreadsheets/d/1ZVXiJXXLH9H52tG4iBJtHB0mmt8mDtzDUu5688hX8zE/edit?usp=sharing")
        elif text=="Abdulkadir":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/spreadsheets/d/1lBTneuuUtgVy2CsMNLeeCZ8a9pkTp_B8Pv-s4yMlulk/edit?usp=sharing")
        elif text=="Hilal":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/spreadsheets/d/1zjLtSviiUEMTBKEYzXg-0VTg4Ph1lEMBes3BduT3Lm0/edit?usp=sharing")
        elif text=="Haniya":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/spreadsheets/d/1cYc_piHCQE2M9-4rxONQzRIzydJF0C-lKiujvb3Z-9M/edit?usp=sharing")
        elif text=="Muaz":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/spreadsheets/d/1w3_SiLcshDx00lxf6v_ecVOARn9HxEklIby23v5244Y/edit?usp=sharing")
        elif text=="Mubarek":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/spreadsheets/d/1sWHqQZuYFCIBPNMTliz1TTLUC4yvnPGEfEdPGkt2V6A/edit?usp=sharing")
        elif text=="Musab":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/spreadsheets/d/1pgPHwEfShwxcKT5jqQpLP6fafGMgIgeZ5GPBr65W7Bw/edit?usp=sharing")
        elif text=="Rahmet (Rim)":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/spreadsheets/d/1mjEEgsjlZG2eeqLRSd12dMGBshTugerdazhBgfzowdE/edit?usp=sharing")
        elif text=="Rahmet 05":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/spreadsheets/d/1mWVkJEG7JODJb82oTDgDnLbrnWGbJBPaJPJ1yJ6Epyo/edit?usp=sharing")
        elif text=="Rahmet 06":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/spreadsheets/d/1lmfEKuuNPOurAjbxEKOH8eVrvvNeC6pvUhr0Bo4ydUM/edit?usp=sharing")
        elif text=="Sehmi":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/spreadsheets/d/1l4TUd9zR_W2qZN385mey-s0dGaZvM4yqRa4UGrK3_aA/edit?usp=sharing")
        elif text=="Seid":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/spreadsheets/d/1kOTaAu89qzw41nUKx4bj7Htm1rJ2sZBjBokzdMduQZc/edit?usp=sharing")
        elif text=="Sekina":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/spreadsheets/d/1gpCNhMFJMCOs2LaAuDXIO3pPgEk2Lna28rF_tEyHiEU/edit?usp=sharing")
        elif text=="Yezid":
            await update.message.reply_text("Click the Link below \n\n https://docs.google.com/spreadsheets/d/1epj27ybKl_tkVvVT0_fLg0elJZP97G11Etx8AgD03sc/edit?usp=sharing")
        elif text=='⬅️ Back':
            updatedState= 'student'
            buttons=['Student information', 'Study schedule']
            message= 'Select your Choice'
            await show_keyboard_button(update, context, buttons,updatedState, message)

        





    elif state== 'grade':
        if text=="Grade 1️⃣" or text =="Grade 2️⃣" or text == "Grade 3️⃣" or text=="Grade 4️⃣" or text=="Grade 5️⃣" or text =="Grade 6️⃣" or text == "Grade 7️⃣" or text=="Grade 8️⃣" :
            updatedState= f"{text} language"
            context.user_data['grade']= text
            await select_language(update, context, updatedState)
        elif text=="Grade 9️⃣" or text =="Grade 1️⃣0️⃣" :
             updatedState=f'{text} format'
             context.user_data['grade']= text
             await select_format(update, context, updatedState)
             
             
        elif text == "Grade 1️⃣1️⃣" or text=="Grade 1️⃣2️⃣":
             updatedState=f'{text} catagory'
             context.user_data['grade']= text
             await select_catagory(update,context,updatedState)
        elif text=="👶 KG":
            updatedState="kg language"
            await select_language(update,context,updatedState)
             
        elif text=='⬅️ Back':
            await original_button(update, context)
    elif state=="kg language":
        if text=="Amharic":
            updatedState= "kg amharic"
            buttons=["KG-1","KG-2","KG-3"]
            message="select grade"
            await show_keyboard_button(update,context,buttons,updatedState,message)
        elif text=="Afaan Oromoo":
            await update.message.reply_text("Coming Soon")
        elif text=='⬅️ Back':
            updatedState="kg language"
            await select_language(update,context,updatedState)
    
    elif state=="kg amharic":
        if text=="KG-1":
            try:
                await update.message.reply_document(document="https://t.me/ethiopian_text_book/456")
            except:
                await update.message.reply_document(document="https://t.me/ethiopian_text_book/456?single")

        elif text =="KG-2":
            try:
                await update.message.reply_document(document="https://t.me/ethiopian_text_book/457")
            except:
                await update.message.reply_document(document="https://t.me/ethiopian_text_book/457?single")
        elif text=="KG-3":
            try:
                await update.message.reply_document(document="https://t.me/ethiopian_text_book/458")
            except:
                await update.message.reply_document(document="https://t.me/ethiopian_text_book/458?single")
        elif text =='⬅️ Back':
            updatedState="kg language"
            await select_language(update,context,updatedState)

    
    elif state=="Grade 1️⃣ language":
        if text=="Amharic":
                updatedState="amharic grade 1 format"
                await select_format(update, context, updatedState)
                
        elif text=="Afaan Oromoo":
                updatedState="oromic grade 1 format"
                await select_format(update, context, updatedState)
        elif text=='⬅️ Back':
            updatedState= 'grade'
            buttons=['Grade 1️⃣','Grade 2️⃣','Grade 3️⃣','Grade 4️⃣','Grade 5️⃣','Grade 6️⃣','Grade 7️⃣','Grade 8️⃣','Grade 9️⃣','Grade 1️⃣0️⃣','Grade 1️⃣1️⃣','Grade 1️⃣2️⃣']
            message ='Select grade'
            await show_keyboard_button(update, context, buttons, updatedState,message)
                
    elif state=="Grade 2️⃣ language":
        if text=="Amharic":
                updatedState="amharic grade 2 format"
                await select_format(update, context, updatedState)
                
        elif text=="Afaan Oromoo":
                updatedState="oromic grade 2 format"
                await select_format(update, context, updatedState)
        elif text=='⬅️ Back':
            updatedState= 'grade'
            buttons=['Grade 1️⃣','Grade 2️⃣','Grade 3️⃣','Grade 4️⃣','Grade 5️⃣','Grade 6️⃣','Grade 7️⃣','Grade 8️⃣','Grade 9️⃣','Grade 1️⃣0️⃣','Grade 1️⃣1️⃣','Grade 1️⃣2️⃣']
            message ='Select grade'
            await show_keyboard_button(update, context, buttons, updatedState,message)
                
    elif state=="Grade 3️⃣ language":
        if text=="Amharic":
                updatedState="amharic grade 3 format"
                await select_format(update, context, updatedState)
                
        elif text=="Afaan Oromoo":
                updatedState="oromic grade 3 format"
                await select_format(update, context, updatedState)
        elif text=='⬅️ Back':
            updatedState= 'grade'
            buttons=['Grade 1️⃣','Grade 2️⃣','Grade 3️⃣','Grade 4️⃣','Grade 5️⃣','Grade 6️⃣','Grade 7️⃣','Grade 8️⃣','Grade 9️⃣','Grade 1️⃣0️⃣','Grade 1️⃣1️⃣','Grade 1️⃣2️⃣']
            message ='Select grade'
            await show_keyboard_button(update, context, buttons, updatedState,message)
                
    elif state=="Grade 4️⃣ language":
        if text=="Amharic":
                updatedState="amharic grade 4 format"
                await select_format(update, context, updatedState)
                
        elif text=="Afaan Oromoo":
                updatedState="oromic grade 4 format"
                await select_format(update, context, updatedState)
        elif text=='⬅️ Back':
            updatedState= 'grade'
            buttons=['Grade 1️⃣','Grade 2️⃣','Grade 3️⃣','Grade 4️⃣','Grade 5️⃣','Grade 6️⃣','Grade 7️⃣','Grade 8️⃣','Grade 9️⃣','Grade 1️⃣0️⃣','Grade 1️⃣1️⃣','Grade 1️⃣2️⃣']
            message ='Select grade'
            await show_keyboard_button(update, context, buttons, updatedState,message)
    elif state =="Grade 5️⃣ language" :           
        if text=="Amharic":
                updatedState="amharic grade 5 format"
                await select_format(update, context, updatedState)
                
        elif text=="Afaan Oromoo":
                updatedState="oromic grade 5 format"
                await select_format(update, context, updatedState)
        elif text=='⬅️ Back':
            updatedState= 'grade'
            buttons=['Grade 1️⃣','Grade 2️⃣','Grade 3️⃣','Grade 4️⃣','Grade 5️⃣','Grade 6️⃣','Grade 7️⃣','Grade 8️⃣','Grade 9️⃣','Grade 1️⃣0️⃣','Grade 1️⃣1️⃣','Grade 1️⃣2️⃣']
            message ='Select grade'
            await show_keyboard_button(update, context, buttons, updatedState,message)
                
    elif state=="Grade 6️⃣ language":
        if text=="Amharic":
                updatedState="amharic grade 6 format"
                await select_format(update, context, updatedState)
                
        elif text=="Afaan Oromoo":
                updatedState="oromic grade 6 format"
                await select_format(update, context, updatedState)
        elif text=='⬅️ Back':
            updatedState= 'grade'
            buttons=['Grade 1️⃣','Grade 2️⃣','Grade 3️⃣','Grade 4️⃣','Grade 5️⃣','Grade 6️⃣','Grade 7️⃣','Grade 8️⃣','Grade 9️⃣','Grade 1️⃣0️⃣','Grade 1️⃣1️⃣','Grade 1️⃣2️⃣']
            message ='Select grade'
            await show_keyboard_button(update, context, buttons, updatedState,message)
                
    elif state=="Grade 7️⃣ language":
        if text=="Amharic":
                updatedState="amharic grade 7 format"
                await select_format(update, context, updatedState)
                
        elif text=="Afaan Oromoo":
                updatedState="oromic grade 7 format"
                await select_format(update, context, updatedState)
        elif text=='⬅️ Back':
            updatedState= 'grade'
            buttons=['Grade 1️⃣','Grade 2️⃣','Grade 3️⃣','Grade 4️⃣','Grade 5️⃣','Grade 6️⃣','Grade 7️⃣','Grade 8️⃣','Grade 9️⃣','Grade 1️⃣0️⃣','Grade 1️⃣1️⃣','Grade 1️⃣2️⃣']
            message ='Select grade'
            await show_keyboard_button(update, context, buttons, updatedState,message)
                
    elif state=="Grade 8️⃣ language":
        if text=="Amharic":
                updatedState="amharic grade 8 format"
                await select_format(update, context, updatedState)
                
        elif text=="Afaan Oromoo":
                updatedState="oromic grade 8 format"
                await select_format(update, context, updatedState)
        elif text=='⬅️ Back':
            updatedState= 'grade'
            buttons=['Grade 1️⃣','Grade 2️⃣','Grade 3️⃣','Grade 4️⃣','Grade 5️⃣','Grade 6️⃣','Grade 7️⃣','Grade 8️⃣','Grade 9️⃣','Grade 1️⃣0️⃣','Grade 1️⃣1️⃣','Grade 1️⃣2️⃣']
            message ='Select grade'
            await show_keyboard_button(update, context, buttons, updatedState,message)
                



    elif state== 'Grade 9️⃣ format':
        
        if text=="📄 PDF" :
             updatedState= 'Grade 9️⃣ courses'
             buttons=["🗣 Amharic","🗨 English", "🔢 Math", "🔬 Biology", "🏛 Citizenship", "🗣 Afaan Oromoo", "🚀 Physics", "🧪 Chemistry","🌍 Geography","📜 History", "🖥 ITechnology", '📈 Economics','🏃 Health and Physical Educaton','🎨 Performing Visual Art']
             message="select course"
             await show_keyboard_button(update, context, buttons, updatedState, message)
             
        elif text == "📱 Mobile App":
             await update.message.reply_text("Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_smart_grade9_new.books")
        
        
        elif text=='⬅️ Back':
            updatedState= 'grade'
            buttons=['Grade 1️⃣','Grade 2️⃣','Grade 3️⃣','Grade 4️⃣','Grade 5️⃣','Grade 6️⃣','Grade 7️⃣','Grade 8️⃣','Grade 9️⃣','Grade 1️⃣0️⃣','Grade 1️⃣1️⃣','Grade 1️⃣2️⃣']
            message ='Select grade'
            await show_keyboard_button(update, context, buttons, updatedState,message)

    elif state== 'Grade 1️⃣0️⃣ format':
        
        if text=="📄 PDF" :
             updatedState=f'Grade 1️⃣0️⃣ courses'
             buttons=["🗣 Amharic","🗨 English", "🔢 Math", "🔬 Biology", "🏛 Citizenship", "🗣 Afaan Oromoo", "🚀 Physics", "🧪 Chemistry","🌍 Geography","📜 History" ,"🖥 ITechnology", '📈 Economics','🏃 Health and Physical Educaton','🎨 Performing Visual Art']
             message="select course"
             await show_keyboard_button(update, context, buttons, updatedState, message)
             
        elif text == "📱 Mobile App":
             await update.message.reply_text("Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_smart_grade10_new.books")
        elif text=='⬅️ Back':
            updatedState= 'grade'
            buttons=['Grade 1️⃣','Grade 2️⃣','Grade 3️⃣','Grade 4️⃣','Grade 5️⃣','Grade 6️⃣','Grade 7️⃣','Grade 8️⃣','Grade 9️⃣','Grade 1️⃣0️⃣','Grade 1️⃣1️⃣','Grade 1️⃣2️⃣']
            message ='Select grade'
            await show_keyboard_button(update, context, buttons, updatedState,message)

        
    elif state=="Grade 1️⃣1️⃣ catagory":
        if text=="🌿Natural Science":
                updatedState="natural grade 11 format"
                await select_format(update, context, updatedState)
        elif text=="👥Social Science":
                updatedState="social grade 11 format"
                await select_format(update, context, updatedState)
        elif text=='⬅️ Back':
            updatedState= 'grade'
            buttons=['Grade 1️⃣','Grade 2️⃣','Grade 3️⃣','Grade 4️⃣','Grade 5️⃣','Grade 6️⃣','Grade 7️⃣','Grade 8️⃣','Grade 9️⃣','Grade 1️⃣0️⃣','Grade 1️⃣1️⃣','Grade 1️⃣2️⃣']
            message ='Select grade'
            await show_keyboard_button(update, context, buttons, updatedState,message)
    elif state=="Grade 1️⃣2️⃣ catagory":
        if text=="🌿Natural Science":
                updatedState="natural grade 12 format"
                await select_format(update, context, updatedState)
        elif text=="👥Social Science":
                updatedState="social grade 12 format"
                await select_format(update, context, updatedState)
        elif text=='⬅️ Back':
            updatedState= 'grade'
            buttons=['Grade 1️⃣','Grade 2️⃣','Grade 3️⃣','Grade 4️⃣','Grade 5️⃣','Grade 6️⃣','Grade 7️⃣','Grade 8️⃣','Grade 9️⃣','Grade 1️⃣0️⃣','Grade 1️⃣1️⃣','Grade 1️⃣2️⃣']
            message ='Select grade'
            await show_keyboard_button(update, context, buttons, updatedState,message)


    elif state=="amharic grade 1 format":
        if text=="📄 PDF":
                updatedState="amharic grade 1"
                buttons=["🗣 አማርኛ","🗣🌐 English", "🔢 ሂሳብ", "🔬 አከባቢ ሳይንስ",'🎨 የስነ ጥበባት ትምህርት', '🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት', '✨ የግብረ ገብ ትምህርት']
                message="Select Course"
                await show_keyboard_button(update, context,buttons,updatedState, message)
        elif text=="📱 Mobile App":
                await update.message.reply_text("Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_oromifa_grade1_new.books&hl=en")
        elif text=='⬅️ Back':
            grade= context.user_data.get('grade')
            updatedState=f'{grade} language'
            await select_language(update,context,updatedState)
        
    elif state=="amharic grade 2 format":
        if text=="📄 PDF":
                updatedState="amharic grade 2"
                buttons=["🗣 አማርኛ","🗣🌐 English", "🔢 ሂሳብ", "🔬 አከባቢ ሳይንስ",'🎨 የስነ ጥበባት ትምህርት', '🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት', '✨ የግብረ ገብ ትምህርት']
                message="Select Course"
                await show_keyboard_button(update, context,buttons,updatedState, message)
        elif text=="📱 Mobile App":
                await update.message.reply_text("Click the Link below \n\n ")
        elif text=='⬅️ Back':
            grade= context.user_data.get('grade')
            updatedState=f'{grade} language'
            await select_language(update,context,updatedState)
    
    elif state=="amharic grade 3 format":
        if text=="📄 PDF":
                updatedState="amharic grade 3"
                buttons=["🗣 አማርኛ","🗣🌐 English", "🔢 ሂሳብ", "🔬 አከባቢ ሳይንስ",'🎨 የስነ ጥበባት ትምህርት', '🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት', '✨ የግብረ ገብ ትምህርት']
                message="Select Course"
                await show_keyboard_button(update, context,buttons,updatedState, message)
        elif text=="📱 Mobile App":
                await update.message.reply_text("Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_oromifa_grade3_new.books")
        elif text=='⬅️ Back':
            grade= context.user_data.get('grade')
            updatedState=f'{grade} language'
            await select_language(update,context,updatedState)
    elif state=="amharic grade 4 format":
        if text=="📄 PDF":
                updatedState="amharic grade 4"
                buttons=["🗣 አማርኛ","🗣🌐 English", "🔢 ሂሳብ", "🔬 አከባቢ ሳይንስ",'🎨 የስነ ጥበባት ትምህርት', '🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት', '✨ የግብረ ገብ ትምህርት']
                message="Select Course"
                await show_keyboard_button(update, context,buttons,updatedState, message)
        elif text=="📱 Mobile App":
                await update.message.reply_text("Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_oromifa_grade4.books&hl=en")
        elif text=='⬅️ Back':
            grade= context.user_data.get('grade')
            updatedState=f'{grade} language'
            await select_language(update,context,updatedState)
    elif state=="amharic grade 5 format":
        if text=="📄 PDF":
                updatedState="amharic grade 5"
                buttons=["🗣 አማርኛ","🗣🌐 English","🗣 Afaan Oromoo", "🔢 ሂሳብ", "🔬 አከባቢ ሳይንስ",'🎨 የስነ ጥበባት ትምህርት', '🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት', '✨ የግብረ ገብ ትምህርት']
                message="Select Course"
                await show_keyboard_button(update, context,buttons,updatedState, message)
        elif text=="📱 Mobile App":
                await update.message.reply_text("Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_oromifa_grade5_new.books")
        elif text=='⬅️ Back':
            grade= context.user_data.get('grade')
            updatedState=f'{grade} language'
            await select_language(update,context,updatedState)
    elif state=="amharic grade 6 format":
        if text=="📄 PDF":
                updatedState="amharic grade 6"
                buttons=["🗣 አማርኛ","🗣🌐 English","🗣 Afaan Oromoo", "🔢 ሂሳብ", "🔬 አከባቢ ሳይንስ",'🎨 የስነ ጥበባት ትምህርት', '🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት', '✨ የግብረ ገብ ትምህርት']
                message="Select Course"
                await show_keyboard_button(update, context,buttons,updatedState, message)
        elif text=="📱 Mobile App":
                await update.message.reply_text("Click the Link below \n\n ")
        elif text=='⬅️ Back':
            grade= context.user_data.get('grade')
            updatedState=f'{grade} language'
            await select_language(update,context,updatedState)
            
    elif state=="amharic grade 7 format":
        if text=="📄 PDF":
                updatedState="amharic grade 7"
                buttons=["🗣 አማርኛ","🗣🌐 English","🗣 Afaan Oromoo", "🔢 ሂሳብ", "🔬 አጠቃላይ ሳይንስ", "👥 የህብረተሰብ ትምህርት", "🏛 ዜግነት", "🎨 የስነ ጥበባት ትምህርት", "🖥 ITechnology", "🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት", "👨‍🔧 ሙያ እና ቴክኒካል ትምህርት"]
                message="Select Course"
                await show_keyboard_button(update, context,buttons,updatedState, message)
        elif text=="📱 Mobile App":
                await update.message.reply_text("Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_oromifa_grade7_new.books")
        elif text=='⬅️ Back':
            grade= context.user_data.get('grade')
            updatedState=f'{grade} language'
            await select_language(update,context,updatedState)
    elif state=="amharic grade 8 format":
        if text=="📄 PDF":
                updatedState="amharic grade 8"
                buttons=["🗣 አማርኛ","🗣🌐 English","🗣 Afaan Oromoo", "🔢 ሂሳብ", "🔬 አጠቃላይ ሳይንስ", "👥 የህብረተሰብ ትምህርት", "🏛 ዜግነት", "🎨 የስነ ጥበባት ትምህርት", "🖥 ITechnology", "🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት", "👨‍🔧 ሙያ እና ቴክኒካል ትምህርት"]
                message="Select Course"
                await show_keyboard_button(update, context,buttons,updatedState, message)
        elif text=="📱 Mobile App":
                await update.message.reply_text("Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_oromifa_grade8_new.books")
        elif text=='⬅️ Back':
            grade= context.user_data.get('grade')
            updatedState=f'{grade} language'
            await select_language(update,context,updatedState)


    elif state=="oromic grade 1 format":
        if text=="📱 Mobile App":
                await update.message.reply_text("Click the Link below \n\n ")
        elif text=='⬅️ Back':
            grade= context.user_data.get('grade')
            updatedState=f'{grade} language'
            await select_language(update,context,updatedState)
        elif text=="📄 PDF":
                updatedState="oromic grade 1"
                buttons=["🗣 Afaan Oromoo","🗣🌐 English", "🔢 Herrega", "🔬 Saayinsii Nannoo",'🎨 Og-aartiiwwan', '🏃 Fayyaafi Jabeenya Qaamaa', '✨ Barnoota Safuu', "⚖️ Gadaa"]
                message="Select Course"
                await show_keyboard_button(update, context,buttons,updatedState, message)
    elif state=="oromic grade 2 format":
        if text=="📱 Mobile App":
                await update.message.reply_text("Click the Link below \n\n ")
        elif text=='⬅️ Back':
            grade= context.user_data.get('grade')
            updatedState=f'{grade} language'
            await select_language(update,context,updatedState)
        elif text=="📄 PDF":
                updatedState="oromic grade 2"
                buttons=["🗣 Afaan Oromoo","🗣🌐 English", "🔢 Herrega", "🔬 Saayinsii Nannoo",'🎨 Og-aartiiwwan', '🏃 Fayyaafi Jabeenya Qaamaa', '✨ Barnoota Safuu', "⚖️ Gadaa"]
                message="Select Course"
                await show_keyboard_button(update, context,buttons,updatedState, message)
    elif state=="oromic grade 3 format":
        if text=="📱 Mobile App":
                await update.message.reply_text("Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_oromifa_grade3_new.books")
        elif text=='⬅️ Back':
            grade= context.user_data.get('grade')
            updatedState=f'{grade} language'
            await select_language(update,context,updatedState)
        elif text=="📄 PDF":
                updatedState="oromic grade 3"
                buttons=["🗣 Afaan Oromoo","🗣🌐 English", "🔢 Herrega", "🔬 Saayinsii Nannoo",'🎨 Og-aartiiwwan', '🏃 Fayyaafi Jabeenya Qaamaa', '✨ Barnoota Safuu', "⚖️ Gadaa"]
                message="Select Course"
                await show_keyboard_button(update, context,buttons,updatedState, message)
    elif state=="oromic grade 4 format":
        if text=="📱 Mobile App":
                await update.message.reply_text("Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_oromifa_grade4.books&hl=en")
        elif text=='⬅️ Back':
            grade= context.user_data.get('grade')
            updatedState=f'{grade} language'
            await select_language(update,context,updatedState)
        elif text=="📄 PDF":
                updatedState="oromic grade 4"
                buttons=["🗣 Afaan Oromoo","🗣🌐 English", "🔢 Herrega", "🔬 Saayinsii Nannoo",'🎨 Og-aartiiwwan', '🏃 Fayyaafi Jabeenya Qaamaa', '✨ Barnoota Safuu', "⚖️ Gadaa"]
                message="Select Course"
                await show_keyboard_button(update, context,buttons,updatedState, message)
    elif state=="oromic grade 5 format":
        if text=="📱 Mobile App":
                await update.message.reply_text("Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_oromifa_grade5_new.books")
        elif text=='⬅️ Back':
            grade= context.user_data.get('grade')
            updatedState=f'{grade} language'
            await select_language(update,context,updatedState)
        elif text=="📄 PDF":
                updatedState="oromic grade 5"
                buttons=["🗣 Afaan Oromoo","🗣🌐 English","🗣 Afaan Amaaraa", "🔢 Herrega", "🔬 Saayinsii Nannoo",'🎨 Og-aartiiwwan', '🏃 Fayyaafi Jabeenya Qaamaa', '✨ Barnoota Safuu', "⚖️ Gadaa"]
                message="Select Course"
                await show_keyboard_button(update, context,buttons,updatedState, message)
    elif state=="oromic grade 6 format":
        if text=="📱 Mobile App":
                await update.message.reply_text("Click the Link below \n\n ")
        elif text=='⬅️ Back':
            grade= context.user_data.get('grade')
            updatedState=f'{grade} language'
            await select_language(update,context,updatedState)
        elif text=="📄 PDF":
                updatedState="oromic grade 6"
                buttons=["🗣 Afaan Oromoo","🗣🌐 English","🗣 Afaan Amaaraa", "🔢 Herrega", "🔬 Saayinsii Nannoo",'🎨 Og-aartiiwwan', '🏃 Fayyaafi Jabeenya Qaamaa', '✨ Barnoota Safuu', "⚖️ Gadaa"]
                message="Select Course"
                await show_keyboard_button(update, context,buttons,updatedState, message)
    elif state=="oromic grade 7 format":
        if text=="📱 Mobile App":
                await update.message.reply_text("Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_oromifa_grade7_new.books")
        elif text=='⬅️ Back':
            grade= context.user_data.get('grade')
            updatedState=f'{grade} language'
            await select_language(update,context,updatedState)
        elif text=="📄 PDF":
                updatedState="oromic grade 7"
                buttons=["🗣 Afaan Oromoo","🗣🌐 English","🗣 Amharic", "🔢 Herrega", "🔬 Saayinsii Waliigalaa","👥 Barnoota Hawaasaa", "🏛 Barnoota Lammummaa",'🎨 Og-aartiiwwan','🖥 ITechnology', '🏃 Fayyaafi Jabeenya Qaamaa', '👨‍🔧 Barnoota Ogummaa fi Teeknikaa', "⚖️ Gadaa"]
                message="Select Course"
                await show_keyboard_button(update, context,buttons,updatedState, message)
    elif state=="oromic grade 8 format":
        if text=="📱 Mobile App":
                await update.message.reply_text("Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_oromifa_grade8_new.books")
        elif text=='⬅️ Back':
            grade= context.user_data.get('grade')
            updatedState=f'{grade} language'
            await select_language(update,context,updatedState)
        elif text=="📄 PDF":
                updatedState="oromic grade 8"
                buttons=["🗣 Afaan Oromoo","🗣🌐 English","🗣 Amharic", "🔢 Herrega", "🔬 Saayinsii Waliigalaa","👥 Barnoota Hawaasaa", "🏛 Barnoota Lammummaa",'🎨 Og-aartiiwwan','🖥 ITechnology', '🏃 Fayyaafi Jabeenya Qaamaa', '👨‍🔧 Barnoota Ogummaa fi Teeknikaa', "⚖️ Gadaa"]
                message="Select Course"
                await show_keyboard_button(update, context,buttons,updatedState, message)
    

  

    
    elif state=="Grade 9️⃣ courses":
                
                if text=='🗣 Amharic':
                    photo='https://t.me/amljheyuiodcji/21'
                    course="grade 9 amharic"
                    await show_inlinekeyboard(update,course,photo)

                elif text=='🗨 English':
                    photo='https://t.me/amljheyuiodcji/22'
                    course="grade 9 english"
                    await show_inlinekeyboard(update,course,photo)
                elif text=='🔢 Math':
                    photo='https://t.me/amljheyuiodcji/25'
                    course="grade 9 math"
                    await show_inlinekeyboard(update,course,photo)
                elif text=='🔬 Biology':
                    photo='https://t.me/amljheyuiodcji/29'
                    course="grade 9 biology"
                    await show_inlinekeyboard(update,course,photo)
                elif text=='🏛 Citizenship':
                    photo='https://t.me/amljheyuiodcji/28'
                    course="grade 9 citizenship"
                    await show_inlinekeyboard(update,course,photo)
                elif text=='🗣 Afaan Oromoo':
                    photo='https://t.me/amljheyuiodcji/30'
                    course="grade 9 oromic"
                    await show_inlinekeyboard(update,course,photo)
                elif text=='🚀 Physics':
                    photo='https://t.me/amljheyuiodcji/31'
                    course="grade 9 physics"
                    await show_inlinekeyboard(update,course,photo)
                elif text=='🧪 Chemistry':
                    photo='https://t.me/amljheyuiodcji/32'
                    course="grade 9 chemistry"
                    await show_inlinekeyboard(update,course,photo)
                elif text=='🌍 Geography':
                     photo="https://t.me/amljheyuiodcji/33"
                     course='grade 9 geography'
                     await show_inlinekeyboard(update,course,photo)
                elif text=='📜 History':
                    photo='https://t.me/amljheyuiodcji/34'
                    course="grade 9 history"
                    await show_inlinekeyboard(update,course,photo)
                elif text=='🖥 ITechnology':
                     photo="https://t.me/amljheyuiodcji/35"
                     course='grade 9 ict'
                     await show_inlinekeyboard(update,course,photo)
                elif text=='📈 Economics':
                     photo="https://t.me/amljheyuiodcji/36"
                     course='grade 9 economics'
                     await show_inlinekeyboard(update,course,photo)
                elif text=='🏃 Health and Physical Educaton':
                     photo="https://t.me/amljheyuiodcji/37"
                     course='grade 9 hpe'
                     await show_inlinekeyboard(update,course,photo)
                elif text=='🎨 Performing Visual Art':
                     photo="https://t.me/amljheyuiodcji/38"
                     course='grade 9 art'
                     await show_inlinekeyboard(update,course,photo)
                elif text=='⬅️ Back':
                    grade= context.user_data.get('grade')
                    updatedState=f'{grade} format'
                    await select_format(update, context, updatedState)


               
    elif state=="Grade 1️⃣0️⃣ courses":        
                if text=='🗣 Amharic':
                    photo='https://t.me/amljheyuiodcji/21'
                    course="grade 10 amharic"
                    await show_inlinekeyboard(update,course,photo)
                elif text=='🗨 English':
                    photo='https://t.me/amljheyuiodcji/22'
                    course="grade 10 english"
                    await show_inlinekeyboard(update,course,photo)
                elif text=='🔢 Math':
                    photo='https://t.me/amljheyuiodcji/25'
                    course="grade 10 math"
                    await show_inlinekeyboard(update,course,photo)
                elif text=='🔬 Biology':
                    photo='https://t.me/amljheyuiodcji/29'
                    course="grade 10 biology"
                    await show_inlinekeyboard(update,course,photo)
                elif text=='🏛 Citizenship':
                    photo='https://t.me/amljheyuiodcji/28'
                    course="grade 10 citizenship"
                    await show_inlinekeyboard(update,course,photo)
                elif text=='🗣 Afaan Oromoo':
                    photo='https://t.me/amljheyuiodcji/30'
                    course="grade 10 oromic"
                    await show_inlinekeyboard(update,course,photo)
                elif text=='🚀 Physics':
                    photo='https://t.me/amljheyuiodcji/31'
                    course="grade 10 physics"
                    await show_inlinekeyboard(update,course,photo)
                elif text=='🧪 Chemistry':
                    photo='https://t.me/amljheyuiodcji/32'
                    course="grade 10 chemistry"
                    await show_inlinekeyboard(update,course,photo)
                elif text=='🌍 Geography':
                     photo="https://t.me/amljheyuiodcji/33"
                     course='grade 10 geography'
                     await show_inlinekeyboard(update,course,photo)
                elif text=='📜 History':
                    photo='https://t.me/amljheyuiodcji/34'
                    course="grade 10 history"
                    await show_inlinekeyboard(update,course,photo)
                elif text=='🖥 ITechnology':
                     photo="https://t.me/amljheyuiodcji/35"
                     course='grade 10 ict'
                     await show_inlinekeyboard(update,course,photo)
                elif text=='📈 Economics':
                     photo="https://t.me/amljheyuiodcji/36"
                     course='grade 10 economics'
                     await show_inlinekeyboard(update,course,photo)
                elif text=='🏃 Health and Physical Educaton':
                     photo="https://t.me/amljheyuiodcji/37"
                     course='grade 10 hpe'
                     await show_inlinekeyboard(update,course,photo)
                elif text=='🎨 Performing Visual Art':
                     photo="https://t.me/amljheyuiodcji/38"
                     course='grade 10 art'
                     await show_inlinekeyboard(update,course,photo)
                elif text=='⬅️ Back':
                    grade= context.user_data.get('grade')
                    updatedState=f'{grade} format'
                    await select_format(update, context, updatedState)  

    

    



    elif state=="natural grade 11 format":
        if text=="📄 PDF":
                updatedState="natural grade 11"
                buttons=["🗨 English", "🔢 Math", "🧬 Biology",'🚀 Physics','🧪 Chemistry','🖥 ITechnology', '🌾 Agriculture']
                message="Select Course"
                await show_keyboard_button(update, context,buttons,updatedState, message)
        elif text=="📱 Mobile App":
                await update.message.reply_text("Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_smart_grade11_new.books")
        elif text=='⬅️ Back':
            grade= context.user_data.get('grade')
            updatedState=f'{grade} catagory'
            await select_catagory(update,context,updatedState)


    elif state=="natural grade 12 format":
        if text=="📄 PDF":
                updatedState="natural grade 12"
                buttons=["🗨 English", "🔢 Math", "🧬 Biology",'🚀 Physics','🧪 Chemistry','🖥 ITechnology', '🌾 Agriculture']
                message="Select Course"
                await show_keyboard_button(update, context,buttons,updatedState, message)
        elif text=="📱 Mobile App":
                await update.message.reply_text("Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_smart_grade12_new.books")
        elif text=='⬅️ Back':
            grade= context.user_data.get('grade')
            updatedState=f'{grade} catagory'
            await select_catagory(update,context,updatedState)
        


    elif state=="social grade 11 format":
        if text=="📄 PDF":
                updatedState="social grade 11"
                buttons=["🗨 English", "🔢 Math",'🌍 Geography','📜 History','📈 Economics', '🖥 ITechnology']
                message="Select Course"
                await show_keyboard_button(update, context,buttons,updatedState, message)
        elif text=="📱 Mobile App":
                await update.message.reply_text('coming soon')
        elif text=='⬅️ Back':
                grade= context.user_data.get('grade')
                updatedState=f'{grade} catagory'
                await select_catagory(update,context,updatedState)


    elif state=="social grade 12 format":
        if text=="📄 PDF":
                updatedState="social grade 12"
                buttons=["🗨 English", "🔢 Math",'🌍 Geography','📜 History','📈 Economics', '🖥 ITechnology']
                message="Select Course"
                await show_keyboard_button(update, context,buttons,updatedState, message)
        elif text=="📱 Mobile App":
                await update.message.reply_text('coming soon')
        elif text=='⬅️ Back':
            grade= context.user_data.get('grade')
            updatedState=f'{grade} catagory'
            await select_catagory(update,context,updatedState)
    
  
    elif state== 'amharic grade 1':
        if text== "🗣 አማርኛ":
            photo='https://t.me/amljheyuiodcji/21'
            course='amharic grade 1 amharic'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🗣🌐 English":
            photo='https://t.me/amljheyuiodcji/22'
            course='amharic grade 1 english'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔢 ሂሳብ":
            photo='https://t.me/amljheyuiodcji/25'
            course='amharic grade 1 math'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔬 አከባቢ ሳይንስ":
            photo='https://t.me/amljheyuiodcji/26'
            course='amharic grade 1 science'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🎨 የስነ ጥበባት ትምህርት":
            photo='https://t.me/amljheyuiodcji/38'
            course='amharic grade 1 art'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት":
            photo='https://t.me/amljheyuiodcji/37'
            course='amharic grade 1 health'
            await show_inlinekeyboard(update,course,photo)
        elif text== "✨ የግብረ ገብ ትምህርት":
            photo='https://t.me/amljheyuiodcji/27'
            course='amharic grade 1 moral'
            await show_inlinekeyboard(update,course,photo)
        elif text=='⬅️ Back':
            updatedState="amharic grade 1 format"
            await select_format(update, context, updatedState)



    elif state== 'oromic grade 1':
        if text== "🗣 Afaan Oromoo":
            photo='https://t.me/amljheyuiodcji/30'
            course='oromic grade 1 afaan oromoo'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🗣🌐 English":
            photo='https://t.me/amljheyuiodcji/22'
            course='oromic grade 1 english'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔢 Herrega":
            photo='https://t.me/amljheyuiodcji/25'
            course='oromic grade 1 math'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔬 Saayinsii Nannoo":
            photo='https://t.me/amljheyuiodcji/26'
            course='oromic grade 1 science'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🎨 Og-aartiiwwan":
            photo='https://t.me/amljheyuiodcji/38'
            course='oromic grade 1 art'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🏃 Fayyaafi Jabeenya Qaamaa":
            photo='https://t.me/amljheyuiodcji/37'
            course='oromic grade 1 health'
            await show_inlinekeyboard(update,course,photo)
        elif text== "✨ Barnoota Safuu":
            photo='https://t.me/amljheyuiodcji/27'
            course='oromic grade 1 moral'
            await show_inlinekeyboard(update,course,photo)
        elif text== "⚖️ Gadaa":
            photo='https://t.me/amljheyuiodcji/39'
            course='oromic grade 1 geda'
            await show_inlinekeyboard(update,course,photo)
        elif text=='⬅️ Back':
            updatedState="oromic grade 1 format"
            await select_format(update, context, updatedState)





    elif state== 'amharic grade 2':
        if text== "🗣 አማርኛ":
            photo='https://t.me/amljheyuiodcji/21'
            course='amharic grade 2 amharic'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🗣🌐 English":
            photo='https://t.me/amljheyuiodcji/22'
            course='amharic grade 2 english'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔢 ሂሳብ":
            photo='https://t.me/amljheyuiodcji/25'
            course='amharic grade 2 math'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔬 አከባቢ ሳይንስ":
            photo='https://t.me/amljheyuiodcji/26'
            course='amharic grade 2 science'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🎨 የስነ ጥበባት ትምህርት":
            photo='https://t.me/amljheyuiodcji/38'
            course='amharic grade 2 art'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት":
            photo='https://t.me/amljheyuiodcji/37'
            course='amharic grade 2 health'
            await show_inlinekeyboard(update,course,photo)
        elif text== "✨ የግብረ ገብ ትምህርት":
            photo='https://t.me/amljheyuiodcji/27'
            course='amharic grade 2 moral'
            await show_inlinekeyboard(update,course,photo)
        elif text=='⬅️ Back':
            updatedState="amharic grade 2 format"
            await select_format(update, context, updatedState)

    elif state== 'oromic grade 2':
        if text== "🗣 Afaan Oromoo":
            photo='https://t.me/amljheyuiodcji/30'
            course='oromic grade 2 afaan oromoo'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🗣🌐 English":
            photo='https://t.me/amljheyuiodcji/22'
            course='oromic grade 2 english'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔢 Herrega":
            photo='https://t.me/amljheyuiodcji/25'
            course='oromic grade 2 math'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔬 Saayinsii Nannoo":
            photo='https://t.me/amljheyuiodcji/26'
            course='oromic grade 2 science'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🎨 Og-aartiiwwan":
            photo='https://t.me/amljheyuiodcji/38'
            course='oromic grade 2 art'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🏃 Fayyaafi Jabeenya Qaamaa":
            photo='https://t.me/amljheyuiodcji/37'
            course='oromic grade 2 health'
            await show_inlinekeyboard(update,course,photo)
        elif text== "✨ Barnoota Safuu":
            photo='https://t.me/amljheyuiodcji/27'
            course='oromic grade 2 moral'
            await show_inlinekeyboard(update,course,photo)
        elif text== "⚖️ Gadaa":
            photo='https://t.me/amljheyuiodcji/39'
            course='oromic grade 2 geda'
            await show_inlinekeyboard(update,course,photo)
        elif text=='⬅️ Back':
            updatedState="oromic grade 2 format"
            await select_format(update, context, updatedState)





    elif state== 'amharic grade 3':
        if text== "🗣 አማርኛ":
            photo='https://t.me/amljheyuiodcji/21'
            course='amharic grade 3 amharic'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🗣🌐 English":
            photo='https://t.me/amljheyuiodcji/22'
            course='amharic grade 3 english'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔢 ሂሳብ":
            photo='https://t.me/amljheyuiodcji/25'
            course='amharic grade 3 math'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔬 አከባቢ ሳይንስ":
            photo='https://t.me/amljheyuiodcji/26'
            course='amharic grade 3 science'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🎨 የስነ ጥበባት ትምህርት":
            photo='https://t.me/amljheyuiodcji/38'
            course='amharic grade 3 art'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት":
            photo='https://t.me/amljheyuiodcji/37'
            course='amharic grade 3 health'
            await show_inlinekeyboard(update,course,photo)
        elif text== "✨ የግብረ ገብ ትምህርት":
            photo='https://t.me/amljheyuiodcji/27'
            course='amharic grade 3 moral'
            await show_inlinekeyboard(update,course,photo)
        elif text=='⬅️ Back':
            updatedState="amharic grade 3 format"
            await select_format(update, context, updatedState)

    elif state== 'oromic grade 3':
        if text== "🗣 Afaan Oromoo":
            photo='https://t.me/amljheyuiodcji/30'
            course='oromic grade 3 afaan oromoo'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🗣🌐 English":
            photo='https://t.me/amljheyuiodcji/22'
            course='oromic grade 3 english'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔢 Herrega":
            photo='https://t.me/amljheyuiodcji/25'
            course='oromic grade 3 math'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔬 Saayinsii Nannoo":
            photo='https://t.me/amljheyuiodcji/26'
            course='oromic grade 3 science'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🎨 Og-aartiiwwan":
            photo='https://t.me/amljheyuiodcji/38'
            course='oromic grade 3 art'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🏃 Fayyaafi Jabeenya Qaamaa":
            photo='https://t.me/amljheyuiodcji/37'
            course='oromic grade 3 health'
            await show_inlinekeyboard(update,course,photo)
        elif text== "✨ Barnoota Safuu":
            photo='https://t.me/amljheyuiodcji/27'
            course='oromic grade 3 moral'
            await show_inlinekeyboard(update,course,photo)
        elif text== "⚖️ Gadaa":
            photo='https://t.me/amljheyuiodcji/39'
            course='oromic grade 3 geda'
            await show_inlinekeyboard(update,course,photo)
        elif text=='⬅️ Back':
            updatedState="oromic grade 3 format"
            await select_format(update, context, updatedState)


    

    elif state== 'amharic grade 4':
        if text== "🗣 አማርኛ":
            photo='https://t.me/amljheyuiodcji/21'
            course='amharic grade 4 amharic'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🗣🌐 English":
            photo='https://t.me/amljheyuiodcji/22'
            course='amharic grade 4 english'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔢 ሂሳብ":
            photo='https://t.me/amljheyuiodcji/25'
            course='amharic grade 4 math'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔬 አከባቢ ሳይንስ":
            photo='https://t.me/amljheyuiodcji/26'
            course='amharic grade 4 science'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🎨 የስነ ጥበባት ትምህርት":
            photo='https://t.me/amljheyuiodcji/38'
            course='amharic grade 4 art'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት":
            photo='https://t.me/amljheyuiodcji/37'
            course='amharic grade 4 health'
            await show_inlinekeyboard(update,course,photo)
        elif text== "✨ የግብረ ገብ ትምህርት":
            photo='https://t.me/amljheyuiodcji/27'
            course='amharic grade 4 moral'
            await show_inlinekeyboard(update,course,photo)
        elif text=='⬅️ Back':
            updatedState="amharic grade 4 format"
            await select_format(update, context, updatedState)

    elif state== 'oromic grade 4':
        if text== "🗣 Afaan Oromoo":
            photo='https://t.me/amljheyuiodcji/30'
            course='oromic grade 4 afaan oromoo'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🗣🌐 English":
            photo='https://t.me/amljheyuiodcji/22'
            course='oromic grade 4 english'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔢 Herrega":
            photo='https://t.me/amljheyuiodcji/25'
            course='oromic grade 4 math'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔬 Saayinsii Nannoo":
            photo='https://t.me/amljheyuiodcji/26'
            course='oromic grade 4 science'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🎨 Og-aartiiwwan":
            photo='https://t.me/amljheyuiodcji/38'
            course='oromic grade 4 art'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🏃 Fayyaafi Jabeenya Qaamaa":
            photo='https://t.me/amljheyuiodcji/37'
            course='oromic grade 4 health'
            await show_inlinekeyboard(update,course,photo)
        elif text== "✨ Barnoota Safuu":
            photo='https://t.me/amljheyuiodcji/27'
            course='oromic grade 4 moral'
            await show_inlinekeyboard(update,course,photo)
        elif text== "⚖️ Gadaa":
            photo='https://t.me/amljheyuiodcji/39'
            course='oromic grade 4 geda'
            await show_inlinekeyboard(update,course,photo)
        elif text=='⬅️ Back':
            updatedState="oromic grade 4 format"
            await select_format(update, context, updatedState)




    elif state== 'amharic grade 5':
        if text== "🗣 አማርኛ":
            photo='https://t.me/amljheyuiodcji/21'
            course='amharic grade 5 amharic'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🗣🌐 English":
            photo='https://t.me/amljheyuiodcji/22'
            course='amharic grade 5 english'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🗣 Afaan Oromoo":
            photo='https://t.me/amljheyuiodcji/30'
            course='amharic grade 5 afaan oromoo'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔢 ሂሳብ":
            photo='https://t.me/amljheyuiodcji/25'
            course='amharic grade 5 math'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔬 አከባቢ ሳይንስ":
            photo='https://t.me/amljheyuiodcji/26'
            course='amharic grade 5 science'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🎨 የስነ ጥበባት ትምህርት":
            photo='https://t.me/amljheyuiodcji/38'
            course='amharic grade 5 art'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት":
            photo='https://t.me/amljheyuiodcji/37'
            course='amharic grade 5 health'
            await show_inlinekeyboard(update,course,photo)
        elif text== "✨ የግብረ ገብ ትምህርት":
            photo='https://t.me/amljheyuiodcji/27'
            course='amharic grade 5 moral'
            await show_inlinekeyboard(update,course,photo)
        elif text=='⬅️ Back':
            updatedState="amharic grade 5 format"
            await select_format(update, context, updatedState)

    elif state== 'oromic grade 5':
        if text== "🗣 Afaan Oromoo":
            photo='https://t.me/amljheyuiodcji/30'
            course='oromic grade 5 afaan oromoo'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🗣🌐 English":
            photo='https://t.me/amljheyuiodcji/22'
            course='oromic grade 5 english'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🗣 Afaan Amaaraa":
            photo='https://t.me/amljheyuiodcji/21'
            course='oromic grade 5 amharic'  
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔢 Herrega":
            photo='https://t.me/amljheyuiodcji/25'
            course='oromic grade 5 math'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔬 Saayinsii Nannoo":
            photo='https://t.me/amljheyuiodcji/26'
            course='oromic grade 5 science'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🎨 Og-aartiiwwan":
            photo='https://t.me/amljheyuiodcji/38'
            course='oromic grade 5 art'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🏃 Fayyaafi Jabeenya Qaamaa":
            photo='https://t.me/amljheyuiodcji/37'
            course='oromic grade 5 health'
            await show_inlinekeyboard(update,course,photo)
        elif text== "✨ Barnoota Safuu":
            photo='https://t.me/amljheyuiodcji/27'
            course='oromic grade 5 moral'
            await show_inlinekeyboard(update,course,photo)
        elif text== "⚖️ Gadaa":
            photo='https://t.me/amljheyuiodcji/39'
            course='oromic grade 5 geda'
            await show_inlinekeyboard(update,course,photo)
        elif text=='⬅️ Back':
            updatedState="oromic grade 5 format"
            await select_format(update, context, updatedState)




    elif state== 'amharic grade 6':
        if text== "🗣 አማርኛ":
            photo='https://t.me/amljheyuiodcji/21'
            course='amharic grade 6 amharic'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🗣🌐 English":
            photo='https://t.me/amljheyuiodcji/22'
            course='amharic grade 6 english'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🗣 Afaan Oromoo":
            photo='https://t.me/amljheyuiodcji/30'
            course='amharic grade 6 afaan oromoo'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔢 ሂሳብ":
            photo='https://t.me/amljheyuiodcji/25'
            course='amharic grade 6 math'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔬 አከባቢ ሳይንስ":
            photo='https://t.me/amljheyuiodcji/26'
            course='amharic grade 1 science'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🎨 የስነ ጥበባት ትምህርት":
            photo='https://t.me/amljheyuiodcji/38'
            course='amharic grade 6 art'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት":
            photo='https://t.me/amljheyuiodcji/37'
            course='amharic grade 6 health'
            await show_inlinekeyboard(update,course,photo)
        elif text== "✨ የግብረ ገብ ትምህርት":
            photo='https://t.me/amljheyuiodcji/27'
            course='amharic grade 6 moral'
            await show_inlinekeyboard(update,course,photo)
        elif text=='⬅️ Back':
            updatedState="amharic grade 6 format"
            await select_format(update, context, updatedState)

    elif state== 'oromic grade 6':
        if text== "🗣 Afaan Oromoo":
            photo='https://t.me/amljheyuiodcji/30'
            course='oromic grade 6 afaan oromoo'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🗣🌐 English":
            photo='https://t.me/amljheyuiodcji/22'
            course='oromic grade 6 english'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🗣 Afaan Amaaraa":
            photo='https://t.me/amljheyuiodcji/21'
            course='oromic grade 6 amharic'  
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔢 Herrega":
            photo='https://t.me/amljheyuiodcji/25'
            course='oromic grade 6 math'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔬 Saayinsii Nannoo":
            photo='https://t.me/amljheyuiodcji/26'
            course='oromic grade 6 science'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🎨 Og-aartiiwwan":
            photo='https://t.me/amljheyuiodcji/38'
            course='oromic grade 6 art'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🏃 Fayyaafi Jabeenya Qaamaa":
            photo='https://t.me/amljheyuiodcji/37'
            course='oromic grade 6 health'
            await show_inlinekeyboard(update,course,photo)
        elif text== "✨ Barnoota Safuu":
            photo='https://t.me/amljheyuiodcji/27'
            course='oromic grade 6 moral'
            await show_inlinekeyboard(update,course,photo)
        elif text== "⚖️ Gadaa":
            photo='https://t.me/amljheyuiodcji/39'
            course='oromic grade 6 geda'
            await show_inlinekeyboard(update,course,photo)
        elif text=='⬅️ Back':
            updatedState="oromic grade 6 format"
            await select_format(update, context, updatedState)


    elif state== 'amharic grade 7':
        if text== "🗣 አማርኛ":
            photo='https://t.me/amljheyuiodcji/21'
            course='amharic grade 7 amharic'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🗣🌐 English":
            photo='https://t.me/amljheyuiodcji/22'
            course='amharic grade 7 english'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🗣 Afaan Oromoo":
            photo='https://t.me/amljheyuiodcji/30'
            course='amharic grade 7 afaan oromoo'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔢 ሂሳብ":
            photo='https://t.me/amljheyuiodcji/25'
            course='amharic grade 7 math'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔬 አጠቃላይ ሳይንስ":
            photo='https://t.me/amljheyuiodcji/40'
            course='amharic grade 7 science'
            await show_inlinekeyboard(update,course,photo)
        elif text== "👥 የህብረተሰብ ትምህርት":
            photo='https://t.me/amljheyuiodcji/41'
            course='amharic grade 7 social studies'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🏛 ዜግነት":
            photo='https://t.me/amljheyuiodcji/28'
            course='amharic grade 7 civics'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🎨 የስነ ጥበባት ትምህርት":
            photo='https://t.me/amljheyuiodcji/38'
            course='amharic grade 7 art'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🖥 ITechnology":
            photo='https://t.me/amljheyuiodcji/35'
            course='amharic grade 7 IT'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት":
            photo='https://t.me/amljheyuiodcji/37'
            course='amharic grade 7 health'
            await show_inlinekeyboard(update,course,photo)
        elif text== "👨‍🔧 ሙያ እና ቴክኒካል ትምህርት":
            photo='https://t.me/amljheyuiodcji/42'
            course='amharic grade 7 vocation'
            await show_inlinekeyboard(update,course,photo)
        elif text=='⬅️ Back':
            updatedState="amharic grade 7 format"
            await select_format(update, context, updatedState)



    elif state== 'oromic grade 7':
        if text== "🗣 Afaan Oromoo":
            photo='https://t.me/amljheyuiodcji/30'
            course='oromic grade 7 afaan oromoo'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🗣🌐 English":
            photo='https://t.me/amljheyuiodcji/22'
            course='oromic grade 7 english'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🗣 Amharic":
            photo='https://t.me/amljheyuiodcji/21'
            course='oromic grade 7 amharic'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔢 Herrega":
            photo='https://t.me/amljheyuiodcji/25'
            course='oromic grade 7 math'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔬 Saayinsii Waliigalaa":
            photo='https://t.me/amljheyuiodcji/40'
            course='oromic grade 7 science'
            await show_inlinekeyboard(update,course,photo)
        elif text== "👥 Barnoota Hawaasaa":
            photo='https://t.me/amljheyuiodcji/41'
            course='oromic grade 7 social studies'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🏛 Barnoota Lammummaa":
            photo='https://t.me/amljheyuiodcji/28'
            course='oromic grade 7 civics'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🎨 Og-aartiiwwan":
            photo='https://t.me/amljheyuiodcji/38'
            course='oromic grade 7 art'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🖥 ITechnology":
            photo='https://t.me/amljheyuiodcji/35'
            course='oromic grade 7 IT'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🏃 Fayyaafi Jabeenya Qaamaa":
            photo='https://t.me/amljheyuiodcji/37'
            course='oromic grade 7 health'
            await show_inlinekeyboard(update,course,photo)
        elif text== "👨‍🔧 Barnoota Ogummaa fi Teeknikaa":
            photo='https://t.me/amljheyuiodcji/42'
            course='oromic grade 7 vocation'
            await show_inlinekeyboard(update,course,photo)
        elif text== "⚖️ Gadaa":
            photo='https://t.me/amljheyuiodcji/39'
            course='oromic grade 7 geda'
            await show_inlinekeyboard(update,course,photo)
        elif text=='⬅️ Back':
            updatedState="oromic grade 7 format"
            await select_format(update, context, updatedState)






    elif state== 'amharic grade 8':
        if text== "🗣 አማርኛ":
            photo='https://t.me/amljheyuiodcji/21'
            course='amharic grade 8 amharic'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🗣🌐 English":
            photo='https://t.me/amljheyuiodcji/22'
            course='amharic grade 8 english'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🗣 Afaan Oromoo":
            photo='https://t.me/amljheyuiodcji/30'
            course='amharic grade 8 afaan oromoo'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔢 ሂሳብ":
            photo='https://t.me/amljheyuiodcji/25'
            course='amharic grade 8 math'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔬 አጠቃላይ ሳይንስ":
            photo='https://t.me/amljheyuiodcji/40'
            course='amharic grade 8 science'
            await show_inlinekeyboard(update,course,photo)
        elif text== "👥 የህብረተሰብ ትምህርት":
            photo='https://t.me/amljheyuiodcji/41'
            course='amharic grade 8 social studies'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🏛 ዜግነት":
            photo='https://t.me/amljheyuiodcji/28'
            course='amharic grade 8 civics'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🎨 የስነ ጥበባት ትምህርት":
            photo='https://t.me/amljheyuiodcji/38'
            course='amharic grade 8 art'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🖥 ITechnology":
            photo='https://t.me/amljheyuiodcji/35'
            course='amharic grade 8 IT'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት":
            photo='https://t.me/amljheyuiodcji/37'
            course='amharic grade 8 health'
            await show_inlinekeyboard(update,course,photo)
        elif text== "👨‍🔧 ሙያ እና ቴክኒካል ትምህርት":
            photo='https://t.me/amljheyuiodcji/42'
            course='amharic grade 8 vocation'
            await show_inlinekeyboard(update,course,photo)
        elif text=='⬅️ Back':
            updatedState="amharic grade 8 format"
            await select_format(update, context, updatedState)

    elif state== 'oromic grade 8':
        if text== "🗣 Afaan Oromoo":
            photo='https://t.me/amljheyuiodcji/30'
            course='oromic grade 8 afaan oromoo'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🗣🌐 English":
            photo='https://t.me/amljheyuiodcji/22'
            course='oromic grade 8 english'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🗣 Amharic":
            photo='https://t.me/amljheyuiodcji/21'
            course='oromic grade 8 amharic'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔢 Herrega":
            photo='https://t.me/amljheyuiodcji/25'
            course='oromic grade 8 math'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔬 Saayinsii Waliigalaa":
            photo='https://t.me/amljheyuiodcji/40'
            course='oromic grade 8 science'
            await show_inlinekeyboard(update,course,photo)
        elif text== "👥 Barnoota Hawaasaa":
            photo='https://t.me/amljheyuiodcji/41'
            course='oromic grade 8 social studies'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🏛 Barnoota Lammummaa":
            photo='https://t.me/amljheyuiodcji/28'
            course='oromic grade 8 civics'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🎨 Og-aartiiwwan":
            photo='https://t.me/amljheyuiodcji/38'
            course='oromic grade 8 art'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🖥 ITechnology":
            photo='https://t.me/amljheyuiodcji/35'
            course='oromic grade 8 IT'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🏃 Fayyaafi Jabeenya Qaamaa":
            photo='https://t.me/amljheyuiodcji/37'
            course='oromic grade 8 health'
            await show_inlinekeyboard(update,course,photo)
        elif text== "👨‍🔧 Barnoota Ogummaa fi Teeknikaa":
            photo='https://t.me/amljheyuiodcji/42'
            course='oromic grade 8 vocation'
            await show_inlinekeyboard(update,course,photo)
        elif text== "⚖️ Gadaa":
            photo='https://t.me/amljheyuiodcji/39'
            course='oromic grade 8 geda'
            await show_inlinekeyboard(update,course,photo)
        elif text=='⬅️ Back':
            updatedState="oromic grade 8 format"
            await select_format(update, context, updatedState)


            ######### grade 11#############3
    
    elif state== 'natural grade 11':
       
        if text== "🗨 English":
            photo='https://t.me/amljheyuiodcji/22'
            course='grade 11 english'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔢 Math":
            photo='https://t.me/amljheyuiodcji/25'
            course='grade 11 math'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🧬 Biology":
            photo='https://t.me/amljheyuiodcji/29'
            course='grade 11 biology'
            await show_inlinekeyboard(update,course,photo)
    
        elif text== "🌾 Agriculture":
            photo='https://t.me/amljheyuiodcji/43'
            course='grade 11 agriculture'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🚀 Physics":
            photo='https://t.me/amljheyuiodcji/31'
            course='grade 11 physics'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🧪 Chemistry":
            photo='https://t.me/amljheyuiodcji/32'
            course='grade 11 chemistry'
            await show_inlinekeyboard(update,course,photo)
        elif text=="🖥 ITechnology":
            photo='https://t.me/amljheyuiodcji/35'
            course='grade 11 ict'
            await show_inlinekeyboard(update,course,photo)
        elif text=='⬅️ Back':
            updatedState="natural grade 11 format"
            await select_format(update, context, updatedState)



             

    elif state== 'social grade 11':
        
        if text== "🗨 English":
            photo='https://t.me/amljheyuiodcji/22'
            course='grade 11 english'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔢 Math":
            photo='https://t.me/amljheyuiodcji/25'
            course='grade 11 math'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🌍 Geography":
            photo='https://t.me/amljheyuiodcji/33'
            course='grade 11 geography'
            await show_inlinekeyboard(update,course,photo)
        elif text== "📜 History":
            photo='https://t.me/amljheyuiodcji/34'
            course='grade 11 history'
            await show_inlinekeyboard(update,course,photo)
        elif text== "📈 Economics":
            photo='https://t.me/amljheyuiodcji/36'
            course='grade 11 economics'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🖥 ITechnology":
            photo='https://t.me/amljheyuiodcji/35'
            course='grade 11 ict'
            await show_inlinekeyboard(update,course,photo)
        
        elif text=='⬅️ Back':
            updatedState="social grade 11 format"
            await select_format(update, context, updatedState)



    elif state== 'natural grade 12':
        if text== "🗨 English":
            photo='https://t.me/amljheyuiodcji/22'
            course='grade 12 english'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔢 Math":
            photo='https://t.me/amljheyuiodcji/25'
            course='grade 12 math'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🧬 Biology":
            photo='https://t.me/amljheyuiodcji/29'
            course='grade 12 biology'
            await show_inlinekeyboard(update,course,photo)
    
        elif text== "🌾 Agriculture":
            photo='https://t.me/amljheyuiodcji/43'
            course='grade 12 agriculture'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🚀 Physics":
            photo='https://t.me/amljheyuiodcji/31'
            course='grade 12 physics'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🧪 Chemistry":
            photo='https://t.me/amljheyuiodcji/32'
            course='grade 12 chemistry'
            await show_inlinekeyboard(update,course,photo)
        elif text=="🖥 ITechnology":
            photo='https://t.me/amljheyuiodcji/35'
            course='grade 12 ict'
            await show_inlinekeyboard(update,course,photo)
        elif text=='⬅️ Back':
            updatedState="natural grade 12 format"
            await select_format(update, context, updatedState)



    elif state== 'social grade 12':
    
        if text== "🗨 English":
            photo='https://t.me/amljheyuiodcji/22'
            course='grade 12 english'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🔢 Math":
            photo='https://t.me/amljheyuiodcji/25'
            course='grade 12 math'
            await show_inlinekeyboard(update,course,photo)
        elif text== "📜 History":
            photo='https://t.me/amljheyuiodcji/34'
            course='grade 12 history'
            await show_inlinekeyboard(update,course,photo)
        elif text== "🌍 Geography":
            photo='https://t.me/amljheyuiodcji/33'
            course='grade 12 geography'
            await show_inlinekeyboard(update,course,photo)
        elif text== "📈 Economics":
            photo='https://t.me/amljheyuiodcji/36'
            course='grade 12 economics'
            await show_inlinekeyboard(update,course,photo)
        elif text=="🖥 ITechnology":
            photo='https://t.me/amljheyuiodcji/35'
            course='grade 12 ict'
            await show_inlinekeyboard(update,course,photo)
        elif text=='⬅️ Back':
            updatedState="social grade 12 format"
            await select_format(update, context, updatedState)
    
    await persistence.update_user_data(update.effective_user.id, context.user_data)



async def button_click(update, context):
    query= update.callback_query
    button_clicked=query.data
    user_name='https://t.me/ethiopian_text_book'
    chat_id=query.message.chat_id

    if button_clicked== 'amharic grade 1 amharic text book':
        id=[47]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 1 amharic reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 1 amharic teachers guide":
        id=[269]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 1 amharic question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 1 english text book':
        id=[48]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 1 english reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 1 english teachers guide":
        id=[272]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 1 english question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 1 math text book':
        id=[49]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 1 math reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 1 math teachers guide":
        id=[274]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 1 math question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 1 science text book':
        id=[46]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 1 science reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 1 science teachers guide":
        id=[276]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 1 science question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 1 art text book':
        id=[50]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 1 art reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 1 art teachers guide":
        id=[275]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 1 art question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 1 health text book':
        id=[51]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 1 health reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 1 health teachers guide":
        id=[270]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 1 health question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 1 moral text book':
        id=[472]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 1 moral reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 1 moral teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 1 moral question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    if button_clicked== 'amharic grade 2 amharic text book':
        id=[66]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 2 amharic reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 2 amharic teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 2 amharic question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 2 english text book':
        id=[67]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 2 english reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 2 english teachers guide":
        id=[285]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 2 english question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 2 math text book':
        id=[69]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 2 math reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 2 math teachers guide":
        id=[286]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 2 math question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 2 science text book':
        id=[65]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 2 science reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 2 science teachers guide":
        id=[288]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 2 science question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 2 art text book':
        id=[64]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 2 art reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 2 art teachers guide":
        id=[287]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 2 art question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 2 health text book':
        id=[68]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 2 health reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 2 health teachers guide":
        id=[284]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 2 health question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 2 moral text book':
        id=[467]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 2 moral reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 2 moral teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 2 moral question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    if button_clicked== 'amharic grade 3 amharic text book':
        id=[83]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 3 amharic reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 3 amharic teachers guide":
        id=[298]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 3 amharic question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 3 english text book':
        id=[85]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 3 english reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 3 english teachers guide":
        id=[300]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 3 english question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 3 math text book':
        id=[86]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 3 math reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 3 math teachers guide":
        id=[301]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 3 math question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 3 science text book':
        id=[82]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 3 science reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 3 science teachers guide":
        id=[303]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 3 science question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 3 art text book':
        id=[81]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 3 art reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 3 art teachers guide":
        id=[302]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 3 art question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 3 health text book':
        id=[84]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 3 health reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 3 health teachers guide":
        id=[299]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 3 health question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 3 moral text book':
        id=[468]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 3 moral reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 3 moral teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 3 moral question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 4 amharic text book':
        id=[98]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 4 amharic reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 4 amharic teachers guide":
        id=[311]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 4 amharic question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 4 english text book':
        id=[100]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 4 english reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 4 english teachers guide":
        id=[313]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 4 english question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 4 math text book':
        id=[101]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 4 math reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 4 math teachers guide":
        id=[314]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 4 math question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 4 science text book':
        id=[475]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 4 science reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 4 science teachers guide":
        id=[316]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 4 science question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 4 art text book':
        id=[474]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 4 art reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 4 art teachers guide":
        id=[315]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 4 art question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 4 health text book':
        id=[99]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 4 health reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 4 health teachers guide":
        id=[312]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 4 health question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 4 moral text book':
        id=[469]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 4 moral reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 4 moral teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 4 moral question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 5 amharic text book':
        id=[117]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 5 amharic reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 5 amharic teachers guide":
        id=[327]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 5 amharic question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 5 english text book':
        id=[119]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 5 english reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 5 english teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 5 english question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 5 afaan oromoo text book':
        id=[118]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 5 afaan oromoo reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 5 afaan oromoo teachers guide":
        id=[331]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 5 afaan oromoo question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 5 math text book':
        id=[120]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 5 math reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 5 math teachers guide":
        id=[329]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 5 math question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 5 science text book':
        id=[116]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 5 science reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 5 science teachers guide":
        id=[326]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 5 science question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 5 art text book':
        id=[115]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 5 art reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 5 art teachers guide":
        id=[332]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 5 art question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 5 health text book':
        id=[121]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 5 health reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 5 health teachers guide":
        id=[328]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 5 health question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 5 moral text book':
        id=[470]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 5 moral reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 5 moral teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 5 moral question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 6 amharic text book':
        id=[137]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 6 amharic reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 6 amharic teachers guide":
        id=[342]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 6 amharic question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 6 english text book':
        id=[138]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 6 english reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 6 english teachers guide":
        id=[341]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 6 english question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 6 afaan oromoo text book':
        id=[136]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 6 afaan oromoo reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 6 afaan oromoo teachers guide":
        id=[346]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 6 afaan oromoo question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 6 math text book':
        id=[140]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 6 math reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 6 math teachers guide":
        id=[344]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 6 math question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 6 science text book':
        id=[135]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 6 science reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 6 science teachers guide":
        id=[347]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 6 science question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 6 art text book':
        id=[134]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 6 art reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 6 art teachers guide":
        id=[345]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 6 art question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 6 health text book':
        id=[139]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 6 health reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 6 health teachers guide":
        id=[343]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 6 health question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 6 moral text book':
        id=[471]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 6 moral reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 6 moral teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 6 moral question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 7 amharic text book':
        id=[154]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 amharic reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 amharic teachers guide":
        id=[358]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 amharic question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 7 english text book':
        id=[159]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 english reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 english teachers guide":
        id=[359]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 english question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 7 afaan oromoo text book':
        id=[155]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 afaan oromoo reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 afaan oromoo teachers guide":
        id=[360]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 afaan oromoo question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 7 math text book':
        id=[160]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 math reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 math teachers guide":
        id=[363]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 math question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 7 science text book':
        id=[162]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 science reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 science teachers guide":
        id=[365]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 science question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 7 social studies text book':
        id=[161]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 social studies reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 social studies teachers guide":
        id=[364]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 social studies question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 7 civics text book':
        id=[157]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 civics reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 civics teachers guide":
        id=[368]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 civics question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    
    elif button_clicked== 'amharic grade 7 art text book':
        id=[153]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 art reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 art teachers guide":
        id=[366]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 art question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 7 IT text book':
        id=[158]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 IT reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 IT teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 IT question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 7 vocation text book':
        id=[477]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 vocation reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 vocation teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 vocation question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 7 health text book':
        id=[156]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 health reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 health teachers guide":
        id=[367]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 health question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 7 moral text book':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 moral reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 moral teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 7 moral question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 8 amharic text book':
        id=[177]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 amharic reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 amharic teachers guide":
        id=[382]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 amharic question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 8 english text book':
        id=[180]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 english reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 english teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 english question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 8 afaan oromoo text book':
        id=[178]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 afaan oromoo reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 afaan oromoo teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 afaan oromoo question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 8 math text book':
        id=[182]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 math reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 math teachers guide":
        id=[386]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 math question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 8 science text book':
        id=[184]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 science reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 science teachers guide":
        id=[389]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 science question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 8 social studies text book':
        id=[185]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 social studies reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 social studies teachers guide":
        id=[390]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 social studies question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 8 civics text book':
        id=[179]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 civics reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 civics teachers guide":
        id=[391]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 civics question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    
    elif button_clicked== 'amharic grade 8 art text book':
        id=[183]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 art reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 art teachers guide":
        id=[388]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 art question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 8 IT text book':
        id=[181]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 IT reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 IT teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 IT question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 8 vocation text book':
        id=[478]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 vocation reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 vocation teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 vocation question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 8 health text book':
        id=[186]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 health reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 health teachers guide":
        id=[381]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 health question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'amharic grade 8 moral text book':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 moral reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 moral teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "amharic grade 8 moral question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    







    elif button_clicked== 'oromic grade 1 afaan oromoo text book':
        id=[57]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 1 afaan oromoo reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 1 afaan oromoo teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 1 afaan oromoo question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 1 english text book':
        id=[53]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 1 english reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 1 english teachers guide":
        id=[278]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 1 english question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 1 math text book':
        id=[56]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 1 math reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 1 math teachers guide":
        id=[281]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 1 math question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 1 science text book':
        id=[59]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 1 science reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 1 science teachers guide":
        id=[279]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 1 science question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 1 art text book':
        id=[58]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 1 art reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 1 art teachers guide":
        id=[282]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 1 art question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 1 health text book':
        id=[54]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 1 health reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 1 health teachers guide":
        id=[280]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 1 health question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 1 moral text book':
        id=[60]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 1 moral reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 1 moral teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 1 moral question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 1 geda text book':
        id=[55]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 1 geda reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 1 geda teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 1 geda question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    
    if button_clicked== 'oromic grade 2 afaan oromoo text book':
        id=[71]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 2 afaan oromoo reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 2 afaan oromoo teachers guide":
        id=[290]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 2 afaan oromoo question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 2 english text book':
        id=[72]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 2 english reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 2 english teachers guide":
        id=[291]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 2 english question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 2 math text book':
        id=[74]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 2 math reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 2 math teachers guide":
        id=[294]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 2 math question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 2 science text book':
        id=[78]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 2 science reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 2 science teachers guide":
        id=[296]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 2 science question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 2 art text book':
        id=[76]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 2 art reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 2 art teachers guide":
        id=[295]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 2 art question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 2 health text book':
        id=[75]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 2 health reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 2 health teachers guide":
        id=[292]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 2 health question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 2 moral text book':
        id=[77]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 2 moral reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 2 moral teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 2 moral question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 2 geda text book':
        id=[73]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 2 geda reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 2 geda teachers guide":
        id=[293]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 2 geda question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    if button_clicked== 'oromic grade 3 afaan oromoo text book':
        id=[92]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 3 afaan oromoo reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 3 afaan oromoo teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 3 afaan oromoo question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 3 english text book':
        id=[88]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 3 english reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 3 english teachers guide":
        id=[305]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 3 english question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 3 math text book':
        id=[91]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 3 math reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 3 math teachers guide":
        id=[308]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 3 math question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 3 science text book':
        id=[94]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 3 science reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 3 science teachers guide":
        id=[306]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 3 science question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 3 art text book':
        id=[93]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 3 art reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 3 art teachers guide":
        id=[309]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 3 art question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 3 health text book':
        id=[89]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 3 health reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 3 health teachers guide":
        id=[307]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 3 health question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 3 moral text book':
        id=[95]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 3 moral reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 3 moral teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 3 moral question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 3 geda text book':
        id=[90]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 3 geda reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 3 geda teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 3 geda question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 4 afaan oromoo text book':
        id=[110]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 4 afaan oromoo reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 4 afaan oromoo teachers guide":
        id=[318]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 4 afaan oromoo question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 4 english text book':
        id=[111]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 4 english reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 4 english teachers guide":
        id=[319]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 4 english question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 4 math text book':
        id=[106]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 4 math reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 4 math teachers guide":
        id=[322]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 4 math question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 4 science text book':
        id=[109]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 4 science reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 4 science teachers guide":
        id=[324]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 4 science question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 4 art text book':
        id=[107]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 4 art reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 4 art teachers guide":
        id=[323]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 4 art question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 4 health text book':
        id=[105]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 4 health reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 4 health teachers guide":
        id=[320]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 4 health question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 4 moral text book':
        id=[108]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 4 moral reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 4 moral teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 4 moral question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 4 geda text book':
        id=[112]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 4 geda reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 4 geda teachers guide":
        id=[321]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 4 geda question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 5 amharic text book':
        id=[128]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 5 amharic reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 5 amharic teachers guide":
        id=[339]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 5 amharic question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 5 english text book':
        id=[124]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 5 english reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 5 english teachers guide":
        id=[334]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 5 english question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 5 afaan oromoo text book':
        id=[123]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 5 afaan oromoo reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 5 afaan oromoo teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 5 afaan oromoo question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 5 math text book':
        id=[127]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 5 math reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 5 math teachers guide":
        id=[338]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 5 math question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 5 science text book':
        id=[130]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 5 science reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 5 science teachers guide":
        id=[335]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 5 science question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 5 art text book':
        id=[129]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 5 art reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 5 art teachers guide":
        id=[337]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 5 art question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 5 health text book':
        id=[125]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 5 health reference":
        id=[336]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 5 health teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 5 health question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 5 moral text book':
        id=[131]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 5 moral reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 5 moral teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 5 moral question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 5 geda text book':
        id=[126]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 5 geda reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 5 geda teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 5 geda question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 6 amharic text book':
        id=[150]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 6 amharic reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 6 amharic teachers guide":
        id=[356]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 6 amharic question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 6 english text book':
        id=[143]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 6 english reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 6 english teachers guide":
        id=[349]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 6 english question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 6 afaan oromoo text book':
        id=[142]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 6 afaan oromoo reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 6 afaan oromoo teachers guide":
        id=[350]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 6 afaan oromoo question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 6 math text book':
        id=[146]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 6 math reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 6 math teachers guide":
        id=[353]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 6 math question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 6 science text book':
        id=[149]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 6 science reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 6 science teachers guide":
        id=[355]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 6 science question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 6 art text book':
        id=[147]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 6 art reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 6 art teachers guide":
        id=[354]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 6 art question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 6 health text book':
        id=[145]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 6 health reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 6 health teachers guide":
        id=[351]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 6 health question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 6 moral text book':
        id=[148]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 6 moral reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 6 moral teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 6 moral question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 7 amharic text book':
        id=[165]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 6 geda text book':
        id=[144]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 6 geda reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 6 geda teachers guide":
        id=[352]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 6 geda question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 amharic reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 amharic teachers guide":
        id=[379]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 amharic question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 7 english text book':
        id=[167]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 english reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 english teachers guide":
        id=[371]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 english question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 7 afaan oromoo text book':
        id=[164]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 afaan oromoo reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 afaan oromoo teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 afaan oromoo question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 7 math text book':
        id=[170]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 math reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 math teachers guide":
        id=[375]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 math question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 7 science text book':
        id=[174]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 science reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 science teachers guide":
        id=[372]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 science question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 7 social studies text book':
        id=[166]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 social studies reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 social studies teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 social studies question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 7 civics text book':
        id=[172]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 civics reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 civics teachers guide":
        id=[370]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 civics question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    
    elif button_clicked== 'oromic grade 7 art text book':
        id=[173]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 art reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 art teachers guide":
        id=[373]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 art question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 7 IT text book':
        id=[171]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 IT reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 IT teachers guide":
        id=[374]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 IT question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 7 vocation text book':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 vocation reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 vocation teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 vocation question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 7 health text book':
        id=[168]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 health reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 health teachers guide":
        id=[376]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 health question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 7 moral text book':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 moral reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 moral teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 moral question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 7 geda text book':
        id=[169]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 geda reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 geda teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 7 geda question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 8 amharic text book':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 amharic reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 amharic teachers guide":
        id=[403]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 amharic question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 8 english text book':
        id=[190]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 english reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 english teachers guide":
        id=[395]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 english question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 8 afaan oromoo text book':
        id=[188]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 afaan oromoo reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 afaan oromoo teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 afaan oromoo question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 8 math text book':
        id=[193]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 math reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 math teachers guide":
        id=[393]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 math question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 8 science text book':
        id=[197]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 science reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 science teachers guide":
        id=[398]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 science question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 8 social studies text book':
        id=[189]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 social studies reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 social studies teachers guide":
        id=[401]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 social studies question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 8 civics text book':
        id=[195]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 civics reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 civics teachers guide":
        id=[394]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 civics question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    
    elif button_clicked== 'oromic grade 8 art text book':
        id=[196]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 art reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 art teachers guide":
        id=[400]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 art question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 8 IT text book':
        id=[194]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 IT reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 IT teachers guide":
        id=[399]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 IT question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 8 vocation text book':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 vocation reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 vocation teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 vocation question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 8 health text book':
        id=[191]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 health reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 health teachers guide":
        id=[396]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 health question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 8 moral text book':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 moral reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 moral teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 moral question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'oromic grade 8 geda text book':
        id=[192]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 geda reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 geda teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "oromic grade 8 geda question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    












    elif button_clicked== 'grade 9 amharic text book':
        id= [204]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 9 amharic reference':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 9 amharic teachers guide':
        id=[406]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 9 amharic question':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 english text book":
        id=[203]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 english reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 english teachers guide":
        id=[410]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 english question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 math text book":
        id=[207]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 math reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 math teachers guide":
        id=[412]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 math question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 biology text book":
        id=[200]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 biology reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 biology teachers guide":
        id=[407]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 biology question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 9 citizenship text book':
        id=[201]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 9 citizenship reference':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 9 citizenship teachers guide':
        id=[409]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 9 citizenship question':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 oromic text book":
        id=[199]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 oromic reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 oromic teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 oromic question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 physics text book":
        id=[211]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 physics reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 physics teachers guide":
        id=[416]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 physics question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 chemistry text book":
        id=[205]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 chemistry reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 chemistry teachers guide":
        id=[408]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 chemistry question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 9 geography text book':
        id=[206]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 9 geography reference':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 9 geography teachers guide':
        id=[411]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 9 geography question':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 history text book":
        id=[208]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 history reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 history teachers guide":
        id=[413]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 history question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 ict text book":
        id=[210]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 ict reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 ict teachers guide":
        id=[415]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 ict question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 economics text book":
        id=[202]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 economics reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 economics teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 economics question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 hpe text book":
        id=[209]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 hpe reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 hpe teachers guide":
        id=[414]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 hpe question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 art text book":
        id=[212]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 art reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 art teachers guide":
        id=[417]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 9 art question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)

    

    elif button_clicked== 'grade 10 amharic text book':
        id=[215]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 10 amharic reference':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 10 amharic teachers guide':
        id=[419]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 10 amharic question':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 english text book":
        id=[220]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 english reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 english teachers guide":
        id=[424]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 english question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 math text book":
        id=[225]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 math reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 math teachers guide":
        id=[430]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 math question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 biology text book":
        id=[216]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 biology reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 biology teachers guide":
        id=[420]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 biology question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 10 citizenship text book':
        id=[218]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 10 citizenship reference':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 10 citizenship teachers guide':
        id=[422]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 10 citizenship question':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 oromic text book":
        id=[214]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 oromic reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 oromic teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 oromic question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 physics text book":
        id=[226]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 physics reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 physics teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 physics question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)

    elif button_clicked== "grade 10 chemistry text book":
        id=[217]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 chemistry reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 chemistry teachers guide":
        id=[421]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 chemistry question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 10 geography text book':
        id=[221]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 10 geography reference':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 10 geography teachers guide':
        id=[425]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 10 geography question':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 history text book":
        id=[222]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 history reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 history teachers guide":
        id=[427]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 history question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 ict text book":
        id=[224]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 ict reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 ict teachers guide":
        id=[429]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 ict question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 economics text book":
        id=[219]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 economics reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 economics teachers guide":
        id=[423]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 economics question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 hpe text book":
        id=[223]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 hpe reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 hpe teachers guide":
        id=[428]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 hpe question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 art text book":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 art reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 art teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 10 art question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)





    elif button_clicked== 'grade 11 english text book':
        id=[232]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 11 english reference':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 11 english teachers guide':
        id=[434]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 11 english question':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 math text book":
        id=[234]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 math reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 math teachers guide":
        id=[436]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 math question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 biology text book":
        id=[230]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 biology reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 biology teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 biology question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 agriculture text book":
        id=[229]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 agriculture reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 agriculture teachers guide":
        id=[432]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 agriculture question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 11 physics text book':
        id=[235]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 11 physics reference':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 11 physics teachers guide':
        id=[437]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 11 physics question':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 chemistry text book":
        id=[231]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 chemistry reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 chemistry teachers guide":
        id=[433]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 chemistry question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 ict text book":
        id=[233]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 ict reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 ict teachers guide":
        id=[435]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 ict question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)





    elif button_clicked== 'grade 12 english text book':
        id=[256]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 12 english reference':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 12 english teachers guide':
        id=[449]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 12 english question':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 math text book":
        id=[258]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 math reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 math teachers guide":
        id=[451]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 math question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 biology text book":
        id=[254]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 biology reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 biology teachers guide":
        id=[447]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 biology question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 agriculture text book":
        id=[253]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 agriculture reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 agriculture teachers guide":
        id=[446]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 agriculture question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 12 physics text book':
        id=[259]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 12 physics reference':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 12 physics teachers guide':
        id=[452]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 12 physics question':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 chemistry text book":
        id=[255]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 chemistry reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 chemistry teachers guide":
        id=[448]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 chemistry question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 ict text book":
        id=[257]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 ict reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 ict teachers guide":
        id=[450]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 ict question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)





    elif button_clicked== 'grade 11 english text book':
        id=[238]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 11 english reference':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 11 english teachers guide':
        id=[440]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 11 english question':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 math text book":
        id=[242]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 math reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 math teachers guide":
        id=[444]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 math question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 geography text book":
        id=[239]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 geography reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 geography teachers guide":
        id=[441]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 geography question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 history text book":
        id=[240]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 history reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 history teachers guide":
        id=[442]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 history question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 11 economics text book':
        id=[237]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 11 economics reference':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 11 economics teachers guide':
        id=[439]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 11 economics question':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 ict text book":
        id=[241]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 ict reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 ict teachers guide":
        id=[443]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 11 ict question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)



    elif button_clicked== 'grade 12 english text book':
        id=[262]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 12 english reference':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 12 english teachers guide':
        id=[419]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 12 english question':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 math text book":
        id=[266]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 math reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 math teachers guide":
        id=[424]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 math question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 geography text book":
        id=[263]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 geography reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 geography teachers guide":
        id=[430]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 geographyquestion":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 history text book":
        id=[264]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 history reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 history teachers guide":
        id=[420]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 history question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 12 economics text book':
        id=[261]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 12 economics reference':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 12 economics teachers guide':
        id=[422]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== 'grade 12 economics question':
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 ict text book":
        id=[265]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 ict reference":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 ict teachers guide":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    elif button_clicked== "grade 12 ict question":
        id=[]
        await retrive_data(query, id, user_name, chat_id,button_clicked)
    await persistence.update_user_data(update.effective_user.id, context.user_data)





   


    
    





# def register_application(app):
#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))
#     app.add_handler(CallbackQueryHandler(button_click))
 
# @app.post("/webhook")
# async def webhook(webhook_data: TelegramWebhook):
#     register_application(application)
#     await application.initialize()
#     await application.process_update(
#         Update.de_json(
#             json.loads(json.dumps(webhook_data.dict(), default=lambda o: o.__dict__)),
#             application.bot,
#         )
#     )
#     return {"message": "ok"}  
    
    
# @app.get('/')
# def index():
#     return {"Message":"working"}

def main():
 
    updater = Updater(Bot(TOKEN),Queue(maxsize=0) )
    #dp = updater.dispatcher
    
    app= Application.builder().token(TOKEN).persistence(persistence).build()
    

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

if __name__ == '__main__':
    main() 
    

    







