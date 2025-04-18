from enum import Enum
from dataclasses import dataclass
from typing import Dict, Optional, List

from core.config import Config
from core.states.states import BotState

@dataclass
class StateTransition:
    next_state: Optional[BotState] = None
    reply_text: Optional[str] = None
    reply_markup: Optional[List[List[str]]] = None
    handler: Optional[str] = None  # For complex cases
    photo : Optional[str] = None
    course : Optional[str] = None

class BotStateMachine:
    _transitions: Dict[BotState, Dict[str, StateTransition]] = {
        BotState.START: {
            "Weekly Schedule 🗓️": StateTransition(
                reply_text=F"Click the link \n {Config.WEEKLY_SCHEDULE_DOC}",
            ),
            "Availability 🕰️": StateTransition(
                next_state=BotState.AWAITING_AVAILABILITY,
                reply_text="Select your availability for this upcoming Saturday",
                reply_markup=[
                    "Throughout the day",
                    "During my shift only",
                    "Outside of my shift only",
                    "I can compromise only if it is necessary by...",
                    "Not at all",
                    "Other",
                ]
            ),
            "Course Material 📚": StateTransition(
                next_state=BotState.AWAITING_GRADE,
                reply_text="Select grade",
                reply_markup= Config.GRADE
            ),
            "Student 👨‍🎓": StateTransition(
                next_state=BotState.AWAITING_STUDENT,
                reply_text="Select your Choice",
                reply_markup=[
                    "Student information",
                    "Study schedule",
                ]
            ),
            "Report 📝": StateTransition(
                reply_text = f"Click the link \n This link is only available for amirs and report sector\n\n{Config.REPORT_DOC}",
            ),
            "Contribution 🙌": StateTransition(
                reply_text=f"Click the link \n {Config.CONTRIBUTION_FORM}"
            )
        },
        
        BotState.AWAITING_AVAILABILITY: {
            "Throughout the day": StateTransition(
                handler="handle_availability_selection"
                
            ),
            "During my shift only": StateTransition(
                handler="handle_availability_selection"
                
            ),
            "Outside of my shift only": StateTransition(
                handler="handle_availability_selection"
                
            ),
            "Not at all": StateTransition(
                handler="handle_availability_selection"
                
            ),
            "I can compromise only if it is necessary by...": StateTransition(
                next_state=BotState.AWAITING_NECESSARY,
                reply_text="Tell us what's in your mind"
            ),
            "Other": StateTransition(
                next_state=BotState.AWAITING_NECESSARY,
                reply_text="Tell us what's in your mind"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.START,
                handler="original_button"
            )
        },
        
        BotState.AWAITING_NECESSARY: {
            "*": StateTransition(  # Wildcard for any text input
                next_state=BotState.AWAITING_COURSE_SCHEDULE,
                reply_text="Specify which courses your student should focus on this week\nPlease write all only in one message",
                handler="store_availability"
            )
        },
        
        BotState.AWAITING_COURSE_SCHEDULE: {
            "*": StateTransition(
                next_state=BotState.AWAITING_AVAILABILITY,
                handler="send_course_schedule"
            )
        },
        
        BotState.AWAITING_STUDENT: {
            "Student information": StateTransition(
                next_state=BotState.AWAITING_STUDENT_INFO,
                reply_text="Select your student",
                reply_markup= Config.STUDENTS 
            ),
            "Study schedule": StateTransition(
                next_state=BotState.AWAITING_STUDENT_SCHEDULE,
                reply_text="Select your student",
                reply_markup= Config.STUDENTS 
            ),
            "⬅️ Back": StateTransition(
                handler="original_button"
            )
        },
        
        BotState.AWAITING_STUDENT_INFO: {
           **{student: StateTransition(reply_text=f"Click the Link below \n\n  {Config.STUDENTS_INFO.get(student, 'There is no such student')}") for student in Config.STUDENTS},
            # Add all other student info links here...
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_STUDENT,
                reply_text="Select your Choice",
                reply_markup=[
                    "Student information",
                    "Study schedule",
                ]
            )
        },
        
        BotState.AWAITING_STUDENT_SCHEDULE: {
           **{student: StateTransition(reply_text=f"Click the Link below \n\n  {Config.STUDENTS_SCHEDULE.get(student, 'There is no such student')}") for student in Config.STUDENTS},
            # Add all other student info links here...
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_STUDENT,
                reply_text="Select your Choice",
                reply_markup=[
                    "Student information",
                    "Study schedule",
                ]
            )
        },
        BotState.AWAITING_GRADE: {
            "Grade 1️⃣": StateTransition(
                next_state=BotState.AWAITING_GRADE_1_LANGUAGE,
                handler="select_language"
            ),
            "Grade 2️⃣": StateTransition(
                next_state=BotState.AWAITING_GRADE_2_LANGUAGE,
                handler="select_language"
            ),
            "Grade 3️⃣": StateTransition(
                next_state=BotState.AWAITING_GRADE_3_LANGUAGE,
                handler="select_language"
            ),
            "Grade 4️⃣": StateTransition(
                next_state=BotState.AWAITING_GRADE_4_LANGUAGE,
                handler="select_language"
            ),
            "Grade 5️⃣": StateTransition(
                next_state=BotState.AWAITING_GRADE_5_LANGUAGE,
                handler="select_language"
            ),
            "Grade 6️⃣": StateTransition(
                next_state=BotState.AWAITING_GRADE_6_LANGUAGE,
                handler="select_language"
            ),
            "Grade 7️⃣": StateTransition(
                next_state=BotState.AWAITING_GRADE_7_LANGUAGE,
                handler="select_language"
            ),
            "Grade 8️⃣": StateTransition(
                next_state=BotState.AWAITING_GRADE_8_LANGUAGE,
                handler="select_language"
            ),
            "Grade 9️⃣": StateTransition(
                next_state=BotState.AWAITING_GRADE_9_FORMAT,
                handler="select_format"
            ),
            "Grade 1️⃣0️⃣": StateTransition(
                next_state=BotState.AWAITING_GRADE_10_FORMAT,
                handler="select_format"
            ),
            "Grade 1️⃣1️⃣": StateTransition(
                next_state=BotState.AWAITING_GRADE_11_CATEGORY,
                handler="select_category"
            ),
            "Grade 1️⃣2️⃣": StateTransition(
                next_state=BotState.AWAITING_GRADE_12_CATEGORY,
                handler="select_category"
            ),
            "👶 KG": StateTransition(
                next_state=BotState.AWAITING_KG_LANGUAGE,
                handler="select_language"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.START,
                handler="original_button"
            )
        },
        
        BotState.AWAITING_KG_LANGUAGE: {
            "Amharic": StateTransition(
                next_state=BotState.AWAITING_KG_AMHARIC,
                reply_text="select grade",
                reply_markup=["KG-1", "KG-2", "KG-3"]
            ),
            "Afaan Oromoo": StateTransition(
                reply_text="Coming Soon"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE,
                reply_text="Select grade",
                reply_markup= Config.GRADE
            )
        },
        
        BotState.AWAITING_KG_AMHARIC: {
            "KG-1": StateTransition(
                handler="send_document",
                reply_text ="https://t.me/ethiopian_text_book/456"
            ),
            "KG-2": StateTransition(
                handler="send_document",
                reply_text ="https://t.me/ethiopian_text_book/457"
            ),
            "KG-3": StateTransition(
                handler="send_document",
                reply_text ="https://t.me/ethiopian_text_book/458"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_KG_LANGUAGE,
                handler="select_language"
            )
        },
        
        # Grade 1-8 Language Selection States
        BotState.AWAITING_GRADE_1_LANGUAGE: {
            "Amharic": StateTransition(
                next_state=BotState.AWAITING_AMHARIC_GRADE_1_FORMAT,
                handler="select_format"
            ),
            "Afaan Oromoo": StateTransition(
                next_state=BotState.AWAITING_OROMIC_GRADE_1_FORMAT,
                handler="select_format"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE,
                reply_text="Select grade",
                reply_markup= Config.GRADE
            )
        },
        
        # Similar patterns for grades 2-8
        BotState.AWAITING_GRADE_2_LANGUAGE: {
            "Amharic": StateTransition(
                next_state=BotState.AWAITING_AMHARIC_GRADE_2_FORMAT,
                handler="select_format"
            ),
            "Afaan Oromoo": StateTransition(
                next_state=BotState.AWAITING_OROMIC_GRADE_2_FORMAT,
                handler="select_format"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE,
                reply_text="Select grade",
                reply_markup= Config.GRADE
            
            )
        },
        BotState.AWAITING_GRADE_3_LANGUAGE: {
            "Amharic": StateTransition(
                next_state=BotState.AWAITING_AMHARIC_GRADE_3_FORMAT,
                handler="select_format"
            ),
            "Afaan Oromoo": StateTransition(
                next_state=BotState.AWAITING_OROMIC_GRADE_3_FORMAT,
                handler="select_format"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE,
                reply_text="Select grade",
                reply_markup= Config.GRADE
            
            )
        },

        BotState.AWAITING_GRADE_4_LANGUAGE: {
            "Amharic": StateTransition(
                next_state=BotState.AWAITING_AMHARIC_GRADE_4_FORMAT,
                handler="select_format"
            ),
            "Afaan Oromoo": StateTransition(
                next_state=BotState.AWAITING_OROMIC_GRADE_4_FORMAT,
                handler="select_format"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE,
                reply_text="Select grade",
                reply_markup= Config.GRADE
            
            )
        },

        BotState.AWAITING_GRADE_5_LANGUAGE: {
            "Amharic": StateTransition(
                next_state=BotState.AWAITING_AMHARIC_GRADE_5_FORMAT,
                handler="select_format"
            ),
            "Afaan Oromoo": StateTransition(
                next_state=BotState.AWAITING_OROMIC_GRADE_5_FORMAT,
                handler="select_format"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE,
                reply_text="Select grade",
                reply_markup= Config.GRADE
            
            )
        },
        
        BotState.AWAITING_GRADE_6_LANGUAGE: {
            "Amharic": StateTransition(
                next_state=BotState.AWAITING_AMHARIC_GRADE_6_FORMAT,
                handler="select_format"
            ),
            "Afaan Oromoo": StateTransition(
                next_state=BotState.AWAITING_OROMIC_GRADE_6_FORMAT,
                handler="select_format"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE,
                reply_text="Select grade",
                reply_markup= Config.GRADE
            
            )
        },

        BotState.AWAITING_GRADE_7_LANGUAGE: {
            "Amharic": StateTransition(
                next_state=BotState.AWAITING_AMHARIC_GRADE_7_FORMAT,
                handler="select_format"
            ),
            "Afaan Oromoo": StateTransition(
                next_state=BotState.AWAITING_OROMIC_GRADE_7_FORMAT,
                handler="select_format"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE,
                reply_text="Select grade",
                reply_markup= Config.GRADE
            
            )
        },
        BotState.AWAITING_GRADE_8_LANGUAGE: {
            "Amharic": StateTransition(
                next_state=BotState.AWAITING_AMHARIC_GRADE_8_FORMAT,
                handler="select_format"
            ),
            "Afaan Oromoo": StateTransition(
                next_state=BotState.AWAITING_OROMIC_GRADE_8_FORMAT,
                handler="select_format"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE,
                reply_text="Select grade",
                reply_markup= Config.GRADE
            
            )
        },

        # Format to course selection from grade 1 - 10


        BotState.AWAITING_AMHARIC_GRADE_1_FORMAT: {
            "📄 PDF": StateTransition(
                next_state=BotState.AWAITING_AMHARIC_GRADE_1,
                reply_text="Select Course",
                reply_markup=[
                    "🗣 አማርኛ", "🗣🌐 English",
                    "🔢 ሂሳብ", "🔬 አከባቢ ሳይንስ",
                    "🎨 የስነ ጥበባት ትምህርት",
                    "🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት",
                    "✨ የግብረ ገብ ትምህርት",
                 
                ]
            ),
            "📱 Mobile App": StateTransition(
                reply_text="Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_oromifa_grade1_new.books&hl=en"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE_1_LANGUAGE,
                handler="select_language"

            )
        },

        BotState.AWAITING_AMHARIC_GRADE_2_FORMAT: {
            "📄 PDF": StateTransition(
                next_state=BotState.AWAITING_AMHARIC_GRADE_2,
                reply_text="Select Course",
                reply_markup=[
                    "🗣 አማርኛ", "🗣🌐 English",
                    "🔢 ሂሳብ", "🔬 አከባቢ ሳይንስ",
                    "🎨 የስነ ጥበባት ትምህርት",
                    "🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት",
                    "✨ የግብረ ገብ ትምህርት",
                ]
            ),
            "📱 Mobile App": StateTransition(
                reply_text="Click the Link below \n\n [Mobile App Link]"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE_2_LANGUAGE,
                handler="select_language"

            )
        },

        BotState.AWAITING_AMHARIC_GRADE_3_FORMAT: {
            "📄 PDF": StateTransition(
                next_state=BotState.AWAITING_AMHARIC_GRADE_3,
                reply_text="Select Course",
                reply_markup=[
                    "🗣 አማርኛ", "🗣🌐 English",
                    "🔢 ሂሳብ", "🔬 አከባቢ ሳይንስ",
                    "🎨 የስነ ጥበባት ትምህርት",
                    "🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት",
                    "✨ የግብረ ገብ ትምህርት",
                    
                ]
            ),
            "📱 Mobile App": StateTransition(
                reply_text="Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_oromifa_grade3_new.books"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE_3_LANGUAGE,
                handler="select_language"

            )
        },

        BotState.AWAITING_AMHARIC_GRADE_4_FORMAT: {
            "📄 PDF": StateTransition(
                next_state=BotState.AWAITING_AMHARIC_GRADE_4,
                reply_text="Select Course",
                reply_markup=[
                    "🗣 አማርኛ", "🗣🌐 English",
                    "🔢 ሂሳብ", "🔬 አከባቢ ሳይንስ",
                    "🎨 የስነ ጥበባት ትምህርት",
                    "🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት",
                    "✨ የግብረ ገብ ትምህርት",
                   
                ]
            ),
            "📱 Mobile App": StateTransition(
                reply_text="Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_oromifa_grade4.books&hl=en"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE_4_LANGUAGE,
                handler="select_language"

            )
        },

        BotState.AWAITING_AMHARIC_GRADE_5_FORMAT: {
            "📄 PDF": StateTransition(
                next_state=BotState.AWAITING_AMHARIC_GRADE_5,
                reply_text="Select Course",
                reply_markup=[
                    "🗣 አማርኛ", "🗣🌐 English", "🗣 Afaan Oromoo",
                    "🔢 ሂሳብ", "🔬 አከባቢ ሳይንስ",
                    "🎨 የስነ ጥበባት ትምህርት",
                    "🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት",
                    "✨ የግብረ ገብ ትምህርት",
                ]
            ),
            "📱 Mobile App": StateTransition(
                reply_text="Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_oromifa_grade5_new.books"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE_5_LANGUAGE,
                handler="select_language"

            )
        },

        BotState.AWAITING_AMHARIC_GRADE_6_FORMAT: {
            "📄 PDF": StateTransition(
                next_state=BotState.AWAITING_AMHARIC_GRADE_6,
                reply_text="Select Course",
                reply_markup=[
                    "🗣 አማርኛ", "🗣🌐 English", "🗣 Afaan Oromoo",
                    "🔢 ሂሳብ", "🔬 አከባቢ ሳይንስ",
                    "🎨 የስነ ጥበባት ትምህርት",
                    "🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት",
                    "✨ የግብረ ገብ ትምህርት",
                ]
            ),
            "📱 Mobile App": StateTransition(
                reply_text="Click the Link below \n\n [Mobile App Link]"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE_6_LANGUAGE,
                handler="select_language"

            )
        },

        BotState.AWAITING_AMHARIC_GRADE_7_FORMAT: {
            "📄 PDF": StateTransition(
                next_state=BotState.AWAITING_AMHARIC_GRADE_7,
                reply_text="Select Course",
                reply_markup=[
                    "🗣 አማርኛ", "🗣🌐 English", "🗣 Afaan Oromoo",
                    "🔢 ሂሳብ", "🔬 አጠቃላይ ሳይንስ",
                    "👥 የህብረተሰብ ትምህርት", "🏛 ዜግነት",
                    "🎨 የስነ ጥበባት ትምህርት", "🖥 ITechnology",
                    "🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት",
                    "👨‍🔧 ሙያ እና ቴክኒካል ትምህርት",
                ]
            ),
            "📱 Mobile App": StateTransition(
                reply_text="Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_oromifa_grade7_new.books"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE_7_LANGUAGE,
                handler="select_language"

            )
        },

        BotState.AWAITING_AMHARIC_GRADE_8_FORMAT: {
            "📄 PDF": StateTransition(
                next_state=BotState.AWAITING_AMHARIC_GRADE_8,
                reply_text="Select Course",
                reply_markup=[
                    "🗣 አማርኛ", "🗣🌐 English", "🗣 Afaan Oromoo",
                    "🔢 ሂሳብ", "🔬 አጠቃላይ ሳይንስ",
                    "👥 የህብረተሰብ ትምህርት", "🏛 ዜግነት",
                    "🎨 የስነ ጥበባት ትምህርት", "🖥 ITechnology",
                    "🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት",
                    "👨‍🔧 ሙያ እና ቴክኒካል ትምህርት",
                ]
            ),
            "📱 Mobile App": StateTransition(
                reply_text="Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_oromifa_grade8_new.books"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE_8_LANGUAGE,
                handler="select_language"

            )
        },

        # Format to course selection for Oromic grades 1-8

        BotState.AWAITING_OROMIC_GRADE_1_FORMAT: {
            "📄 PDF": StateTransition(
                next_state=BotState.AWAITING_OROMIC_GRADE_1,
                reply_text="Select Course",
                reply_markup=[
                    "🗣 Afaan Oromoo", "🗣🌐 English",
                    "🔢 Herrega", "🔬 Saayinsii Nannoo",
                    "🎨 Og-aartiiwwan",
                    "🏃 Fayyaafi Jabeenya Qaamaa",
                    "✨ Barnoota Safuu", "⚖️ Gadaa",
                ]
            ),
            "📱 Mobile App": StateTransition(
                reply_text="Click the Link below \n\n [Mobile App Link]"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE_1_LANGUAGE,
                handler="select_language"

            )
        },

        BotState.AWAITING_OROMIC_GRADE_2_FORMAT: {
            "📄 PDF": StateTransition(
                next_state=BotState.AWAITING_OROMIC_GRADE_2,
                reply_text="Select Course",
                reply_markup=[
                    "🗣 Afaan Oromoo", "🗣🌐 English",
                    "🔢 Herrega", "🔬 Saayinsii Nannoo",
                    "🎨 Og-aartiiwwan",
                    "🏃 Fayyaafi Jabeenya Qaamaa",
                    "✨ Barnoota Safuu", "⚖️ Gadaa",
                ]
            ),
            "📱 Mobile App": StateTransition(
                reply_text="Click the Link below \n\n [Mobile App Link]"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE_2_LANGUAGE,
                handler="select_language"

            )
        },

        BotState.AWAITING_OROMIC_GRADE_3_FORMAT: {
            "📄 PDF": StateTransition(
                next_state=BotState.AWAITING_OROMIC_GRADE_3,
                reply_text="Select Course",
                reply_markup=[
                    "🗣 Afaan Oromoo", "🗣🌐 English",
                    "🔢 Herrega", "🔬 Saayinsii Nannoo",
                    "🎨 Og-aartiiwwan",
                    "🏃 Fayyaafi Jabeenya Qaamaa",
                    "✨ Barnoota Safuu", "⚖️ Gadaa",
                ]
            ),
            "📱 Mobile App": StateTransition(
                reply_text="Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_oromifa_grade3_new.books"
            ),
            "⬅️ Back": StateTransition(
        
                next_state=BotState.AWAITING_GRADE_3_LANGUAGE,
                handler="select_language"

            )
        },

        BotState.AWAITING_OROMIC_GRADE_4_FORMAT: {
            "📄 PDF": StateTransition(
                next_state=BotState.AWAITING_OROMIC_GRADE_4,
                reply_text="Select Course",
                reply_markup=[
                    "🗣 Afaan Oromoo", "🗣🌐 English",
                    "🔢 Herrega", "🔬 Saayinsii Nannoo",
                    "🎨 Og-aartiiwwan",
                    "🏃 Fayyaafi Jabeenya Qaamaa",
                    "✨ Barnoota Safuu", "⚖️ Gadaa",
                ]
            ),
            "📱 Mobile App": StateTransition(
                reply_text="Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_oromifa_grade4.books&hl=en"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE_4_LANGUAGE,
                handler="select_language"

            )
        },

        BotState.AWAITING_OROMIC_GRADE_5_FORMAT: {
            "📄 PDF": StateTransition(
                next_state=BotState.AWAITING_OROMIC_GRADE_5,
                reply_text="Select Course",
                reply_markup=[
                    "🗣 Afaan Oromoo", "🗣🌐 English", "🗣 Afaan Amaaraa",
                    "🔢 Herrega", "🔬 Saayinsii Nannoo",
                    "🎨 Og-aartiiwwan",
                    "🏃 Fayyaafi Jabeenya Qaamaa",
                    "✨ Barnoota Safuu", "⚖️ Gadaa",
                ]
            ),
            "📱 Mobile App": StateTransition(
                reply_text="Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_oromifa_grade5_new.books"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE_5_LANGUAGE,
                handler="select_language"

            )
        },

        BotState.AWAITING_OROMIC_GRADE_6_FORMAT: {
            "📄 PDF": StateTransition(
                next_state=BotState.AWAITING_OROMIC_GRADE_6,
                reply_text="Select Course",
                reply_markup=[
                    "🗣 Afaan Oromoo", "🗣🌐 English", "🗣 Afaan Amaaraa",
                    "🔢 Herrega", "🔬 Saayinsii Nannoo",
                    "🎨 Og-aartiiwwan",
                    "🏃 Fayyaafi Jabeenya Qaamaa",
                    "✨ Barnoota Safuu", "⚖️ Gadaa",
                ]
            ),
            "📱 Mobile App": StateTransition(
                reply_text="Click the Link below \n\n [Mobile App Link]"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE_6_LANGUAGE,
                handler="select_language"

            )
        },

        BotState.AWAITING_OROMIC_GRADE_7_FORMAT: {
            "📄 PDF": StateTransition(
                next_state=BotState.AWAITING_OROMIC_GRADE_7,
                reply_text="Select Course",
                reply_markup=[
                    "🗣 Afaan Oromoo", "🗣🌐 English", "🗣 Amharic",
                    "🔢 Herrega", "🔬 Saayinsii Waliigalaa",
                    "👥 Barnoota Hawaasaa", "🏛 Barnoota Lammummaa",
                    "🎨 Og-aartiiwwan", "🖥 ITechnology",
                    "🏃 Fayyaafi Jabeenya Qaamaa",
                    "👨‍🔧 Barnoota Ogummaa fi Teeknikaa", "⚖️ Gadaa",
                ]
            ),
            "📱 Mobile App": StateTransition(
                reply_text="Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_oromifa_grade7_new.books"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE_7_LANGUAGE,
                handler="select_language"

            )
        },

        BotState.AWAITING_OROMIC_GRADE_8_FORMAT: {
            "📄 PDF": StateTransition(
                next_state=BotState.AWAITING_OROMIC_GRADE_8,
                reply_text="Select Course",
                reply_markup=[
                    "🗣 Afaan Oromoo", "🗣🌐 English", "🗣 Amharic",
                    "🔢 Herrega", "🔬 Saayinsii Waliigalaa",
                    "👥 Barnoota Hawaasaa", "🏛 Barnoota Lammummaa",
                    "🎨 Og-aartiiwwan", "🖥 ITechnology",
                    "🏃 Fayyaafi Jabeenya Qaamaa",
                    "👨‍🔧 Barnoota Ogummaa fi Teeknikaa", "⚖️ Gadaa",
                    
                ]
            ),
            "📱 Mobile App": StateTransition(
                reply_text="Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_oromifa_grade8_new.books"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE_8_LANGUAGE,
                handler="select_language"

            )
        },


        # Format to course selection from grade 9 - 12

         BotState.AWAITING_GRADE_9_FORMAT: {
            "📄 PDF": StateTransition(
                next_state=BotState.AWAITING_GRADE_9_COURSES,
                reply_text="Select Course",
                reply_markup= Config.GRADE_9_COURSES
            ),
            "📱 Mobile App": StateTransition(
                reply_text="Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_smart_grade9_new.books"
            ),
           
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE,
                reply_text="Select grade",
                reply_markup= Config.GRADE
            )
        },

        BotState.AWAITING_GRADE_10_FORMAT: {
            "📄 PDF": StateTransition(
                next_state=BotState.AWAITING_GRADE_10_COURSES,
                reply_text="Select Course",
                reply_markup= Config.GRADE_9_COURSES,
            ),
            "📱 Mobile App": StateTransition(
                reply_text="Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_smart_grade10_new.books"
            ),
           
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE,
                reply_text="Select grade",
                reply_markup= Config.GRADE
            )
        },

        BotState.AWAITING_NATURAL_GRADE_11_FORMAT: {
            "📄 PDF": StateTransition(
                next_state=BotState.AWAITING_NATURAL_GRADE_11,
                reply_text="Select Course",
                reply_markup=[
                    "🗨 English", "🔢 Math",
                    "🧬 Biology", "🚀 Physics",
                    "🧪 Chemistry", "🖥 ITechnology",
                    "🌾 Agriculture",
                    
                ]
            ),
            "📱 Mobile App": StateTransition(
                reply_text="Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_smart_grade11_new.books"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE_11_CATEGORY,
                handler="select_category"
            )
        },

        BotState.AWAITING_NATURAL_GRADE_12_FORMAT: {
            "📄 PDF": StateTransition(
                next_state=BotState.AWAITING_NATURAL_GRADE_12,
                reply_text="Select Course",
                reply_markup=[
                    "🗨 English", "🔢 Math",
                    "🧬 Biology", "🚀 Physics",
                    "🧪 Chemistry", "🖥 ITechnology",
                    "🌾 Agriculture",
                    
                ]
            ),
            "📱 Mobile App": StateTransition(
                reply_text="Click the Link below \n\n https://play.google.com/store/apps/details?id=com.ethio_smart_grade12_new.books"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE_12_CATEGORY,
                handler="select_category"
            )
        },

        # Social Science Grade 11 Format
        BotState.AWAITING_SOCIAL_GRADE_11_FORMAT: {
            "📄 PDF": StateTransition(
                next_state=BotState.AWAITING_SOCIAL_GRADE_11,
                reply_text="Select Course",
                reply_markup=[
                    "🗨 English", "🔢 Math",
                    "🌍 Geography", "📜 History",
                    "📈 Economics", "🖥 ITechnology",
                 
                ]
            ),
            "📱 Mobile App": StateTransition(
                reply_text="Coming soon"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE_11_CATEGORY,
                handler="select_category"
            )
        },

        # Social Science Grade 12 Format
        BotState.AWAITING_SOCIAL_GRADE_12_FORMAT: {
            "📄 PDF": StateTransition(
                next_state=BotState.AWAITING_SOCIAL_GRADE_12,
                reply_text="Select Course",
                reply_markup=[
                    "🗨 English", "🔢 Math",
                    "🌍 Geography", "📜 History",
                    "📈 Economics", "🖥 ITechnology",
                 
                ]
            ),
            "📱 Mobile App": StateTransition(
                reply_text="Coming soon"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE_12_CATEGORY,
                handler="select_category"
            )
        },


         # Grade 11-12 Category Selection
        BotState.AWAITING_GRADE_11_CATEGORY: {
            "🌿Natural Science": StateTransition(
                next_state=BotState.AWAITING_NATURAL_GRADE_11_FORMAT,
                handler="select_format"
            ),
            "👥Social Science": StateTransition(
                next_state=BotState.AWAITING_SOCIAL_GRADE_11_FORMAT,
                handler="select_format"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE,
                reply_text="Select grade",
                reply_markup= Config.GRADE
            )
        },

        BotState.AWAITING_GRADE_12_CATEGORY: {
            "🌿Natural Science": StateTransition(
                next_state=BotState.AWAITING_NATURAL_GRADE_12_FORMAT,
                handler="select_format"
            ),
            "👥Social Science": StateTransition(
                next_state=BotState.AWAITING_SOCIAL_GRADE_12_FORMAT,
                handler="select_format"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE,
                reply_text="Select grade",
                reply_markup= Config.GRADE
            )
        },


        # Courses selection from grade 1 - 8

        # Amharic Grade 1 Subjects
        BotState.AWAITING_AMHARIC_GRADE_1: {
            "🗣 አማርኛ": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/21",
                course="amharic grade 1 amharic"
            ),
            "🗣🌐 English": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/22",
                course="amharic grade 1 english"
            ),
            "🔢 ሂሳብ": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/25",
                course="amharic grade 1 math"
            ),
            "🔬 አከባቢ ሳይንስ": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/26",
                course="amharic grade 1 science"
            ),
            "🎨 የስነ ጥበባት ትምህርት": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/38",
                course="amharic grade 1 art"
            ),
            "🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/37",
                course="amharic grade 1 health"
            ),
            "✨ የግብረ ገብ ትምህርት": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/27",
                course="amharic grade 1 moral"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_AMHARIC_GRADE_1_FORMAT,
                handler="select_format"

            )
        },
        BotState.AWAITING_OROMIC_GRADE_1: {
            "🗣 Afaan Oromoo": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/30",
                course="oromic grade 1 afaan oromoo"
            ),
            "🗣🌐 English": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/22",
                course="oromic grade 1 english"
            ),
            "🔢 Herrega": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/25",
                course="oromic grade 1 math"
            ),
            "🔬 Saayinsii Nannoo": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/26",
                course="oromic grade 1 science"
            ),
            "🎨 Og-aartiiwwan": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/38",
                course="oromic grade 1 art"
            ),
            "🏃 Fayyaafi Jabeenya Qaamaa": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/37",
                course="oromic grade 1 health"
            ),
            "✨ Barnoota Safuu": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/27",
                course="oromic grade 1 moral"
            ),
            "⚖️ Gadaa": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/39",
                course="oromic grade 1 geda"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_OROMIC_GRADE_1_FORMAT,
                handler="select_format"
            )
        },

        # Amharic Grade 2 Subjects
        BotState.AWAITING_AMHARIC_GRADE_2: {
            "🗣 አማርኛ": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/21",
                course="amharic grade 2 amharic"
            ),
            "🗣🌐 English": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/22",
                course="amharic grade 2 english"
            ),
            "🔢 ሂሳብ": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/25",
                course="amharic grade 2 math"
            ),
            "🔬 አከባቢ ሳይንስ": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/26",
                course="amharic grade 2 science"
            ),
            "🎨 የስነ ጥበባት ትምህርት": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/38",
                course="amharic grade 2 art"
            ),
            "🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/37",
                course="amharic grade 2 health"
            ),
            "✨ የግብረ ገብ ትምህርት": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/27",
                course="amharic grade 2 moral"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_AMHARIC_GRADE_2_FORMAT,
                handler="select_format"
            )
        },

        # Oromic Grade 2 Subjects
        BotState.AWAITING_OROMIC_GRADE_2: {
            "🗣 Afaan Oromoo": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/30",
                course="oromic grade 2 afaan oromoo"
            ),
            "🗣🌐 English": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/22",
                course="oromic grade 2 english"
            ),
            "🔢 Herrega": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/25",
                course="oromic grade 2 math"
            ),
            "🔬 Saayinsii Nannoo": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/26",
                course="oromic grade 2 science"
            ),
            "🎨 Og-aartiiwwan": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/38",
                course="oromic grade 2 art"
            ),
            "🏃 Fayyaafi Jabeenya Qaamaa": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/37",
                course="oromic grade 2 health"
            ),
            "✨ Barnoota Safuu": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/27",
                course="oromic grade 2 moral"
            ),
            "⚖️ Gadaa": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/39",
                course="oromic grade 2 geda"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_OROMIC_GRADE_2_FORMAT,
                handler="select_format"
            )
        },

        # Amharic Grade 3 Subjects
        BotState.AWAITING_AMHARIC_GRADE_3: {
            "🗣 አማርኛ": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/21",
                course="amharic grade 3 amharic"
            ),
            "🗣🌐 English": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/22",
                course="amharic grade 3 english"
            ),
            "🔢 ሂሳብ": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/25",
                course="amharic grade 3 math"
            ),
            "🔬 አከባቢ ሳይንስ": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/26",
                course="amharic grade 3 science"
            ),
            "🎨 የስነ ጥበባት ትምህርት": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/38",
                course="amharic grade 3 art"
            ),
            "🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/37",
                course="amharic grade 3 health"
            ),
            "✨ የግብረ ገብ ትምህርት": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/27",
                course="amharic grade 3 moral"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_AMHARIC_GRADE_3_FORMAT,
                handler="select_format"
            )
        },

        # Oromic Grade 3 Subjects
        BotState.AWAITING_OROMIC_GRADE_3: {
            "🗣 Afaan Oromoo": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/30",
                course="oromic grade 3 afaan oromoo"
            ),
            "🗣🌐 English": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/22",
                course="oromic grade 3 english"
            ),
            "🔢 Herrega": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/25",
                course="oromic grade 3 math"
            ),
            "🔬 Saayinsii Nannoo": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/26",
                course="oromic grade 3 science"
            ),
            "🎨 Og-aartiiwwan": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/38",
                course="oromic grade 3 art"
            ),
            "🏃 Fayyaafi Jabeenya Qaamaa": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/37",
                course="oromic grade 3 health"
            ),
            "✨ Barnoota Safuu": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/27",
                course="oromic grade 3 moral"
            ),
            "⚖️ Gadaa": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/39",
                course="oromic grade 3 geda"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_OROMIC_GRADE_3_FORMAT,
                handler="select_format"
            )
        },

        BotState.AWAITING_AMHARIC_GRADE_4: {
            "🗣 አማርኛ": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/21",
                course="amharic grade 4 amharic"
            ),
            "🗣🌐 English": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/22",
                course="amharic grade 4 english"
            ),
            "🔢 ሂሳብ": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/25",
                course="amharic grade 4 math"
            ),
            "🔬 አከባቢ ሳይንስ": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/26",
                course="amharic grade 4 science"
            ),
            "🎨 የስነ ጥበባት ትምህርት": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/38",
                course="amharic grade 4 art"
            ),
            "🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/37",
                course="amharic grade 4 health"
            ),
            "✨ የግብረ ገብ ትምህርት": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/27",
                course="amharic grade 4 moral"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_AMHARIC_GRADE_4_FORMAT,
                handler="select_format"
            )
        },

        # Oromic Grade 4 Subjects
        BotState.AWAITING_OROMIC_GRADE_4: {
            "🗣 Afaan Oromoo": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/30",
                course="oromic grade 4 afaan oromoo"
            ),
            "🗣🌐 English": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/22",
                course="oromic grade 4 english"
            ),
            "🔢 Herrega": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/25",
                course="oromic grade 4 math"
            ),
            "🔬 Saayinsii Nannoo": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/26",
                course="oromic grade 4 science"
            ),
            "🎨 Og-aartiiwwan": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/38",
                course="oromic grade 4 art"
            ),
            "🏃 Fayyaafi Jabeenya Qaamaa": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/37",
                course="oromic grade 4 health"
            ),
            "✨ Barnoota Safuu": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/27",
                course="oromic grade 4 moral"
            ),
            "⚖️ Gadaa": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/39",
                course="oromic grade 4 geda"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_OROMIC_GRADE_4_FORMAT,
                handler="select_format"
            )
        },

        # Amharic Grade 5 Subjects
        BotState.AWAITING_AMHARIC_GRADE_5: {
            "🗣 አማርኛ": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/21",
                course="amharic grade 5 amharic"
            ),
            "🗣🌐 English": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/22",
                course="amharic grade 5 english"
            ),
            "🗣 Afaan Oromoo": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/30",
                course="amharic grade 5 afaan oromoo"
            ),
            "🔢 ሂሳብ": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/25",
                course="amharic grade 5 math"
            ),
            "🔬 አከባቢ ሳይንስ": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/26",
                course="amharic grade 5 science"
            ),
            "🎨 የስነ ጥበባት ትምህርት": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/38",
                course="amharic grade 5 art"
            ),
            "🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/37",
                course="amharic grade 5 health"
            ),
            "✨ የግብረ ገብ ትምህርት": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/27",
                course="amharic grade 5 moral"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_AMHARIC_GRADE_5_FORMAT,
                handler="select_format"
            )
        },

        # Oromic Grade 5 Subjects
        BotState.AWAITING_OROMIC_GRADE_5: {
            "🗣 Afaan Oromoo": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/30",
                course="oromic grade 5 afaan oromoo"
            ),
            "🗣🌐 English": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/22",
                course="oromic grade 5 english"
            ),
            "🗣 Afaan Amaaraa": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/21",
                course="oromic grade 5 amharic"
            ),
            "🔢 Herrega": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/25",
                course="oromic grade 5 math"
            ),
            "🔬 Saayinsii Nannoo": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/26",
                course="oromic grade 5 science"
            ),
            "🎨 Og-aartiiwwan": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/38",
                course="oromic grade 5 art"
            ),
            "🏃 Fayyaafi Jabeenya Qaamaa": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/37",
                course="oromic grade 5 health"
            ),
            "✨ Barnoota Safuu": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/27",
                course="oromic grade 5 moral"
            ),
            "⚖️ Gadaa": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/39",
                course="oromic grade 5 geda"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_OROMIC_GRADE_5_FORMAT,
                handler="select_format"
            )
        },

        # Amharic Grade 6 Subjects
        BotState.AWAITING_AMHARIC_GRADE_6: {
            "🗣 አማርኛ": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/21",
                course="amharic grade 6 amharic"
            ),
            "🗣🌐 English": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/22",
                course="amharic grade 6 english"
            ),
            "🗣 Afaan Oromoo": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/30",
                course="amharic grade 6 afaan oromoo"
            ),
            "🔢 ሂሳብ": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/25",
                course="amharic grade 6 math"
            ),
            "🔬 አከባቢ ሳይንስ": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/26",
                course="amharic grade 6 science"
            ),
            "🎨 የስነ ጥበባት ትምህርት": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/38",
                course="amharic grade 6 art"
            ),
            "🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/37",
                course="amharic grade 6 health"
            ),
            "✨ የግብረ ገብ ትምህርት": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/27",
                course="amharic grade 6 moral"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_AMHARIC_GRADE_6_FORMAT,
                handler="select_format"
            )
        },
        BotState.AWAITING_OROMIC_GRADE_6: {
            "🗣 Afaan Oromoo": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/30",
                course="oromic grade 6 afaan oromoo"
            ),
            "🗣🌐 English": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/22",
                course="oromic grade 6 english"
            ),
            "🗣 Afaan Amaaraa": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/21",
                course="oromic grade 6 amharic"
            ),
            "🔢 Herrega": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/25",
                course="oromic grade 6 math"
            ),
            "🔬 Saayinsii Nannoo": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/26",
                course="oromic grade 6 science"
            ),
            "🎨 Og-aartiiwwan": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/38",
                course="oromic grade 6 art"
            ),
            "🏃 Fayyaafi Jabeenya Qaamaa": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/37",
                course="oromic grade 6 health"
            ),
            "✨ Barnoota Safuu": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/27",
                course="oromic grade 6 moral"
            ),
            "⚖️ Gadaa": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/39",
                course="oromic grade 6 geda"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_OROMIC_GRADE_6_FORMAT,
                handler="select_format"
            )
        },

        # Amharic Grade 7 Subjects
        BotState.AWAITING_AMHARIC_GRADE_7: {
            "🗣 አማርኛ": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/21",
                course="amharic grade 7 amharic"
            ),
            "🗣🌐 English": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/22",
                course="amharic grade 7 english"
            ),
            "🗣 Afaan Oromoo": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/30",
                course="amharic grade 7 afaan oromoo"
            ),
            "🔢 ሂሳብ": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/25",
                course="amharic grade 7 math"
            ),
            "🔬 አጠቃላይ ሳይንስ": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/40",
                course="amharic grade 7 science"
            ),
            "👥 የህብረተሰብ ትምህርት": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/41",
                course="amharic grade 7 social studies"
            ),
            "🏛 ዜግነት": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/28",
                course="amharic grade 7 civics"
            ),
            "🎨 የስነ ጥበባት ትምህርት": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/38",
                course="amharic grade 7 art"
            ),
            "🖥 ITechnology": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/35",
                course="amharic grade 7 IT"
            ),
            "🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/37",
                course="amharic grade 7 health"
            ),
            "👨‍🔧 ሙያ እና ቴክኒካል ትምህርት": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/42",
                course="amharic grade 7 vocation"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_AMHARIC_GRADE_7_FORMAT,
                handler="select_format"
            )
        },

        # Oromic Grade 7 Subjects
        BotState.AWAITING_OROMIC_GRADE_7: {
            "🗣 Afaan Oromoo": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/30",
                course="oromic grade 7 afaan oromoo"
            ),
            "🗣🌐 English": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/22",
                course="oromic grade 7 english"
            ),
            "🗣 Amharic": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/21",
                course="oromic grade 7 amharic"
            ),
            "🔢 Herrega": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/25",
                course="oromic grade 7 math"
            ),
            "🔬 Saayinsii Waliigalaa": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/40",
                course="oromic grade 7 science"
            ),
            "👥 Barnoota Hawaasaa": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/41",
                course="oromic grade 7 social studies"
            ),
            "🏛 Barnoota Lammummaa": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/28",
                course="oromic grade 7 civics"
            ),
            "🎨 Og-aartiiwwan": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/38",
                course="oromic grade 7 art"
            ),
            "🖥 ITechnology": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/35",
                course="oromic grade 7 IT"
            ),
            "🏃 Fayyaafi Jabeenya Qaamaa": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/37",
                course="oromic grade 7 health"
            ),
            "👨‍🔧 Barnoota Ogummaa fi Teeknikaa": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/42",
                course="oromic grade 7 vocation"
            ),
            "⚖️ Gadaa": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/39",
                course="oromic grade 7 geda"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_OROMIC_GRADE_7_FORMAT,
                handler="select_format"
            )
        },
        BotState.AWAITING_AMHARIC_GRADE_8: {
            "🗣 አማርኛ": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/21",
                course="amharic grade 8 amharic"
            ),
            "🗣🌐 English": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/22",
                course="amharic grade 8 english"
            ),
            "🗣 Afaan Oromoo": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/30",
                course="amharic grade 8 afaan oromoo"
            ),
            "🔢 ሂሳብ": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/25",
                course="amharic grade 8 math"
            ),
            "🔬 አጠቃላይ ሳይንስ": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/40",
                course="amharic grade 8 science"
            ),
            "👥 የህብረተሰብ ትምህርት": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/41",
                course="amharic grade 8 social studies"
            ),
            "🏛 ዜግነት": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/28",
                course="amharic grade 8 civics"
            ),
            "🎨 የስነ ጥበባት ትምህርት": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/38",
                course="amharic grade 8 art"
            ),
            "🖥 ITechnology": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/35",
                course="amharic grade 8 IT"
            ),
            "🏃 የጤና እና የሰውነት ማጎልመሻ ትምህርት": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/37",
                course="amharic grade 8 health"
            ),
            "👨‍🔧 ሙያ እና ቴክኒካል ትምህርት": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/42",
                course="amharic grade 8 vocation"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_AMHARIC_GRADE_8_FORMAT,
                handler="select_format"
            )
        },

        # Oromic Grade 8 Subjects
        BotState.AWAITING_OROMIC_GRADE_8: {
            "🗣 Afaan Oromoo": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/30",
                course="oromic grade 8 afaan oromoo"
            ),
            "🗣🌐 English": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/22",
                course="oromic grade 8 english"
            ),
            "🗣 Amharic": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/21",
                course="oromic grade 8 amharic"
            ),
            "🔢 Herrega": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/25",
                course="oromic grade 8 math"
            ),
            "🔬 Saayinsii Waliigalaa": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/40",
                course="oromic grade 8 science"
            ),
            "👥 Barnoota Hawaasaa": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/41",
                course="oromic grade 8 social studies"
            ),
            "🏛 Barnoota Lammummaa": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/28",
                course="oromic grade 8 civics"
            ),
            "🎨 Og-aartiiwwan": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/38",
                course="oromic grade 8 art"
            ),
            "🖥 ITechnology": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/35",
                course="oromic grade 8 IT"
            ),
            "🏃 Fayyaafi Jabeenya Qaamaa": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/37",
                course="oromic grade 8 health"
            ),
            "👨‍🔧 Barnoota Ogummaa fi Teeknikaa": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/42",
                course="oromic grade 8 vocation"
            ),
            "⚖️ Gadaa": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/39",
                course="oromic grade 8 geda"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_OROMIC_GRADE_8_FORMAT,
                handler="select_format"
            )
        },

        # Course selection from grade 9 -12

         # Grade 9 Courses Selection
        BotState.AWAITING_GRADE_9_COURSES: {
            "🗣 Amharic": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/21",
                course="grade 9 amharic"
            ),
            "🗨 English": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/22",
                course="grade 9 english"
            ),
            "🔢 Math": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/25",
                course="grade 9 math"
            ),
            "🔬 Biology": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/29",
                course="grade 9 biology"
            ),
            "🏛 Citizenship": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/28",
                course="grade 9 citizenship"
            ),
            "🗣 Afaan Oromoo": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/30",
                course="grade 9 oromic"
            ),
            "🚀 Physics": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/31",
                course="grade 9 physics"
            ),
            "🧪 Chemistry": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/32",
                course="grade 9 chemistry"
            ),
            "🌍 Geography": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/33",
                course="grade 9 geography"
            ),
            "📜 History": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/34",
                course="grade 9 history"
            ),
            "🖥 ITechnology": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/35",
                course="grade 9 ict"
            ),
            "📈 Economics": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/36",
                course="grade 9 economics"
            ),
            "🏃 Health and Physical Educaton": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/37",
                course="grade 9 hpe"
            ),
            "🎨 Performing Visual Art": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/38",
                course="grade 9 art"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE_9_FORMAT,
                handler="select_format"
            )
        },

        BotState.AWAITING_GRADE_10_COURSES: {
            "🗣 Amharic": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/21",
                course="grade 10 amharic"
            ),
            "🗨 English": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/22",
                course="grade 10 english"
            ),
            "🔢 Math": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/25",
                course="grade 10 math"
            ),
            "🔬 Biology": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/29",
                course="grade 10 biology"
            ),
            "🏛 Citizenship": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/28",
                course="grade 10 citizenship"
            ),
            "🗣 Afaan Oromoo": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/30",
                course="grade 10 oromic"
            ),
            "🚀 Physics": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/31",
                course="grade 10 physics"
            ),
            "🧪 Chemistry": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/32",
                course="grade 10 chemistry"
            ),
            "🌍 Geography": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/33",
                course="grade 10 geography"
            ),
            "📜 History": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/34",
                course="grade 10 history"
            ),
            "🖥 ITechnology": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/35",
                course="grade 10 ict"
            ),
            "📈 Economics": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/36",
                course="grade 10 economics"
            ),
            "🏃 Health and Physical Educaton": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/37",
                course="grade 10 hpe"
            ),
            "🎨 Performing Visual Art": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/38",
                course="grade 10 art"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_GRADE_10_FORMAT,
                handler="select_format"
            )
        },

        # Natural Science Grade 11 Subjects
        BotState.AWAITING_NATURAL_GRADE_11: {
            "🗨 English": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/22",
                course="grade 11 english"
            ),
            "🔢 Math": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/25",
                course="grade 11 math"
            ),
            "🧬 Biology": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/29",
                course="grade 11 biology"
            ),
            "🚀 Physics": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/31",
                course="grade 11 physics"
            ),
            "🧪 Chemistry": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/32",
                course="grade 11 chemistry"
            ),
            "🖥 ITechnology": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/35",
                course="grade 11 ict"
            ),
            "🌾 Agriculture": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/43",
                course="grade 11 agriculture"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_NATURAL_GRADE_11_FORMAT,
                handler="select_format"
            )
        },
        BotState.AWAITING_SOCIAL_GRADE_11: {
            "🗨 English": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/22",
                course="grade 11 english"
            ),
            "🔢 Math": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/25",
                course="grade 11 math"
            ),
            "🌍 Geography": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/33",
                course="grade 11 geography"
            ),
            "📜 History": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/34",
                course="grade 11 history"
            ),
            "📈 Economics": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/36",
                course="grade 11 economics"
            ),
            "🖥 ITechnology": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/35",
                course="grade 11 ict"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_SOCIAL_GRADE_11_FORMAT,
                handler="select_format"
            )
        },

        # Natural Science Grade 12 Subjects
        BotState.AWAITING_NATURAL_GRADE_12: {
            "🗨 English": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/22",
                course="grade 12 english"
            ),
            "🔢 Math": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/25",
                course="grade 12 math"
            ),
            "🧬 Biology": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/29",
                course="grade 12 biology"
            ),
            "🚀 Physics": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/31",
                course="grade 12 physics"
            ),
            "🧪 Chemistry": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/32",
                course="grade 12 chemistry"
            ),
            "🖥 ITechnology": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/35",
                course="grade 12 ict"
            ),
            "🌾 Agriculture": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/43",
                course="grade 12 agriculture"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_NATURAL_GRADE_12_FORMAT,
                handler="select_format"
            )
        },

        # Social Science Grade 12 Subjects
        BotState.AWAITING_SOCIAL_GRADE_12: {
            "🗨 English": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/22",
                course="grade 12 english"
            ),
            "🔢 Math": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/25",
                course="grade 12 math"
            ),
            "📜 History": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/34",
                course="grade 12 history"
            ),
            "🌍 Geography": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/33",
                course="grade 12 geography"
            ),
            "📈 Economics": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/36",
                course="grade 12 economics"
            ),
            "🖥 ITechnology": StateTransition(
                handler="show_inlinekeyboard",
                photo="https://t.me/amljheyuiodcji/35",
                course="grade 12 ict"
            ),
            "⬅️ Back": StateTransition(
                next_state=BotState.AWAITING_SOCIAL_GRADE_12_FORMAT,
                handler="select_format"
            )
        }


    }


    
    def get_transition(self, state: BotState, action: str) -> Optional[StateTransition]:
        return self._transitions.get(state, {}).get(action)