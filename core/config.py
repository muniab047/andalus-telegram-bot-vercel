import json
import os
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

class Config:
    # Telegram
    TOKEN = os.getenv("TOKEN")
    DB_URI = os.getenv("DB_URI")
    PORT = int(os.getenv("PORT", "80"))
    BOT = Bot(token=TOKEN)
    CHAT_ID = os.getenv("CHAT_ID")
    GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")
    WEEKLY_SCHEDULE_DOC = os.getenv("WEEKLY_SCHEDULE_DOC")
    REPORT_DOC = os.getenv("REPORT_DOC")
    CONTRIBUTION_FORM = os.getenv("CONTRIBUTION_FORM")
    STUDENTS_INFO = json.loads(os.getenv("STUDENTS_INFO", "[]"))
    STUDENTS_SCHEDULE = json.loads(os.getenv("STUDENTS_SCHEDULE", "[]"))

    # Students
    STUDENTS = [
        'Abas', 'Abdulkadir', 'Abdulmalik', 'Amar', 'Asiya', 'Ferhan', 
        'Hanan', 'Haniya', 'Hilal', 'Rahmet 06', 'Rahmet (Rim)',
        'Muaz', 'Mubarek', 'Musab', 'Rahmet 05', 'Sehmi', 'Seid',
        'Sekina', 'Sifen', 'Yezid'
    ]
    GRADE = [
                    "👶 KG",
                    "Grade 1️⃣",
                    "Grade 2️⃣",
                    "Grade 3️⃣",
                    "Grade 4️⃣",
                    "Grade 5️⃣",
                    "Grade 6️⃣",
                    "Grade 7️⃣",
                    "Grade 8️⃣",
                    "Grade 9️⃣",
                    "Grade 1️⃣0️⃣",
                    "Grade 1️⃣1️⃣",
                    "Grade 1️⃣2️⃣",
                  
                ]
    GRADE_9_COURSES = ["🗣 Amharic","🗨 English", "🔢 Math", "🔬 Biology", "🏛 Citizenship", "🗣 Afaan Oromoo", "🚀 Physics", "🧪 Chemistry","🌍 Geography","📜 History", "🖥 ITechnology", '📈 Economics','🏃 Health and Physical Educaton','🎨 Performing Visual Art']
    

config = Config()