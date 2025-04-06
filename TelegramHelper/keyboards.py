from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Main keyboards for users
def get_client_keyboard(language='en'):
    """Returns the main keyboard for regular users"""
    buttons = {
        'en': [["Log Hours", "Check Hours"], ["History", "Language 🌐"]],
        'ru': [["Записать часы", "Проверить часы"], ["История", "Язык 🌐"]],
        'pl': [["Zapisz godziny", "Sprawdź godziny"], ["Historia", "Język 🌐"]],
        'uk': [["Записати години", "Перевірити години"], ["Історія", "Мова 🌐"]]
    }
    
    # Default to English if language not supported
    lang = language if language in buttons else 'en'
    
    keyboard = []
    for row in buttons[lang]:
        keyboard.append([KeyboardButton(text=btn) for btn in row])
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_language_keyboard():
    """Returns the keyboard for language selection"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")],
            [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
            [InlineKeyboardButton(text="🇵🇱 Polski", callback_data="lang_pl")],
            [InlineKeyboardButton(text="🇺🇦 Українська", callback_data="lang_uk")]
        ]
    )

def get_hour_keyboard():
    """Returns the keyboard for selecting hours"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="1"), 
                KeyboardButton(text="2"), 
                KeyboardButton(text="3"), 
                KeyboardButton(text="4")
            ],
            [KeyboardButton(text="More")]
        ],
        resize_keyboard=True
    )

def get_minute_keyboard():
    """Returns the keyboard for selecting minutes"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="0 minutes"), 
                KeyboardButton(text="15 minutes"),
                KeyboardButton(text="30 minutes"), 
                KeyboardButton(text="45 minutes")
            ]
        ],
        resize_keyboard=True
    )

def get_admin_confirmation_keyboard():
    """Returns the keyboard for admin hour confirmation"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Confirm"), KeyboardButton(text="❌ Reject")]
        ],
        resize_keyboard=True
    )
