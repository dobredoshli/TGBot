"""
Multi-language support for the GK Studio Bot
"""

MESSAGES = {
    'en': {
        'welcome': "Welcome, {}! This bot helps you track your studio hours.",
        'select_hours': "Select the number of full hours:",
        'select_minutes': "Now select the minutes:",
        'custom_hours_prompt': "Enter the number of hours manually (use decimal for partial hours, e.g., 2.5):",
        'hours_sent': "Your hours have been sent for admin approval.",
        'invalid_number': "Please enter a valid number (e.g., 2.5)",
        'non_positive_number': "Please enter a positive number.",
        'hours_confirmed': "Your hours have been confirmed! You have earned {} free session(s) and have {} hours {} minutes recorded for further discounts.",
        'hours_rejected': "Your hours were not approved by the admin.",
        'current_hours': "You have {} hours and {} minutes in the studio.\n",
        'free_sessions': "You have earned {} free session(s)!\n",
        'next_free_session': "You need {} more hours for your next free session.",
        'language_changed': "Language changed to English.",
        'choose_language': "Please select your language:",
        'language_button': "🇬🇧 English",
        'no_logs': "You don't have any hour logs yet.",
        'history_header': "Your recent hour logs:",
        'status_confirmed': "✓ Confirmed",
        'status_pending': "⏳ Pending",
        'hours_text': "{} hours",
        'stats_header': "Studio Statistics",
        'total_users': "Total users: {}",
        'total_hours': "Total hours logged: {:.2f}",
        'average_hours': "Average hours per user: {:.2f}",
        'top_users': "Top {} users by hours:",
        'user_hours': "{} - {:.2f} hours",
        'no_users': "No users in the database.",
        'no_pending_hours': "No hours pending approval.",
        'cannot_confirm_own': "You cannot confirm your own hours.",
        'hours_confirmed_admin': "Hours confirmed for user ID:{}, who now has {} hours and {} minutes.",
        'hours_rejected_admin': "Hours rejected for user ID:{}."
    },
    'ru': {
        'welcome': "Добро пожаловать, {}! Этот бот поможет вам отслеживать часы в студии.",
        'select_hours': "Выберите количество полных часов:",
        'select_minutes': "Теперь выберите минуты:",
        'custom_hours_prompt': "Введите количество часов вручную (используйте десятичную дробь для неполных часов, например, 2.5):",
        'hours_sent': "Ваши часы отправлены на подтверждение администратору.",
        'invalid_number': "Пожалуйста, введите правильное число (например, 2.5)",
        'non_positive_number': "Пожалуйста, введите положительное число.",
        'hours_confirmed': "Ваши часы подтверждены! Вы заработали {} бесплатных сеанс(ов) и у вас осталось {} часов {} минут для дальнейших скидок.",
        'hours_rejected': "Ваши часы не были одобрены администратором.",
        'current_hours': "У вас есть {} часов и {} минут в студии.\n",
        'free_sessions': "Вы заработали {} бесплатных сеанс(ов)!\n",
        'next_free_session': "Вам нужно еще {} часов для следующего бесплатного сеанса.",
        'language_changed': "Язык изменен на русский.",
        'choose_language': "Пожалуйста, выберите язык:",
        'language_button': "🇷🇺 Русский",
        'no_logs': "У вас еще нет записей о часах.",
        'history_header': "Ваши последние записи часов:",
        'status_confirmed': "✓ Подтверждено",
        'status_pending': "⏳ Ожидание",
        'hours_text': "{} часов",
        'stats_header': "Статистика студии",
        'total_users': "Всего пользователей: {}",
        'total_hours': "Всего зарегистрировано часов: {:.2f}",
        'average_hours': "Среднее количество часов на пользователя: {:.2f}",
        'top_users': "Топ-{} пользователей по часам:",
        'user_hours': "{} - {:.2f} часов",
        'no_users': "В базе данных нет пользователей.",
        'no_pending_hours': "Нет часов, ожидающих подтверждения.",
        'cannot_confirm_own': "Вы не можете подтвердить свои собственные часы.",
        'hours_confirmed_admin': "Часы подтверждены для пользователя ID:{}, у него теперь {} часов и {} минут.",
        'hours_rejected_admin': "Часы отклонены для пользователя ID:{}."
    },
    'pl': {
        'welcome': "Witaj, {}! Ten bot pomoże ci śledzić godziny w studiu.",
        'select_hours': "Wybierz liczbę pełnych godzin:",
        'select_minutes': "Teraz wybierz minuty:",
        'custom_hours_prompt': "Wprowadź liczbę godzin ręcznie (użyj ułamka dziesiętnego dla niepełnych godzin, np. 2.5):",
        'hours_sent': "Twoje godziny zostały wysłane do zatwierdzenia przez administratora.",
        'invalid_number': "Proszę wprowadzić prawidłową liczbę (np. 2.5)",
        'non_positive_number': "Proszę wprowadzić liczbę dodatnią.",
        'hours_confirmed': "Twoje godziny zostały potwierdzone! Zarobiłeś {} darmowych sesji i masz {} godzin {} minut zapisanych na przyszłe zniżki.",
        'hours_rejected': "Twoje godziny nie zostały zatwierdzone przez administratora.",
        'current_hours': "Masz {} godzin i {} minut w studiu.\n",
        'free_sessions': "Zarobiłeś {} darmowych sesji!\n",
        'next_free_session': "Potrzebujesz jeszcze {} godzin do następnej darmowej sesji.",
        'language_changed': "Język zmieniony na polski.",
        'choose_language': "Proszę wybrać język:",
        'language_button': "🇵🇱 Polski",
        'no_logs': "Nie masz jeszcze żadnych zapisów godzin.",
        'history_header': "Twoje ostatnie zapisy godzin:",
        'status_confirmed': "✓ Potwierdzone",
        'status_pending': "⏳ Oczekiwanie",
        'hours_text': "{} godzin",
        'stats_header': "Statystyki studia",
        'total_users': "Liczba użytkowników: {}",
        'total_hours': "Łączna liczba zarejestrowanych godzin: {:.2f}",
        'average_hours': "Średnia liczba godzin na użytkownika: {:.2f}",
        'top_users': "Top {} użytkowników według godzin:",
        'user_hours': "{} - {:.2f} godzin",
        'no_users': "Brak użytkowników w bazie danych.",
        'no_pending_hours': "Brak godzin oczekujących na zatwierdzenie.",
        'cannot_confirm_own': "Nie możesz potwierdzić swoich własnych godzin.",
        'hours_confirmed_admin': "Godziny potwierdzone dla użytkownika ID:{}, ma teraz {} godzin i {} minut.",
        'hours_rejected_admin': "Godziny odrzucone dla użytkownika ID:{}."
    },
    'uk': {
        'welcome': "Вітаємо, {}! Цей бот допоможе вам відстежувати години в студії.",
        'select_hours': "Виберіть кількість повних годин:",
        'select_minutes': "Тепер виберіть хвилини:",
        'custom_hours_prompt': "Введіть кількість годин вручну (використовуйте десятковий дріб для неповних годин, наприклад, 2.5):",
        'hours_sent': "Ваші години відправлені на підтвердження адміністратору.",
        'invalid_number': "Будь ласка, введіть правильне число (наприклад, 2.5)",
        'non_positive_number': "Будь ласка, введіть додатне число.",
        'hours_confirmed': "Ваші години підтверджені! Ви заробили {} безкоштовних сеансів і у вас залишилося {} годин {} хвилин для подальших знижок.",
        'hours_rejected': "Ваші години не були схвалені адміністратором.",
        'current_hours': "У вас є {} годин і {} хвилин у студії.\n",
        'free_sessions': "Ви заробили {} безкоштовних сеансів!\n",
        'next_free_session': "Вам потрібно ще {} годин для наступного безкоштовного сеансу.",
        'language_changed': "Мова змінена на українську.",
        'choose_language': "Будь ласка, виберіть мову:",
        'language_button': "🇺🇦 Українська",
        'no_logs': "У вас ще немає записів про години.",
        'history_header': "Ваші останні записи годин:",
        'status_confirmed': "✓ Підтверджено",
        'status_pending': "⏳ Очікування",
        'hours_text': "{} годин",
        'stats_header': "Статистика студії",
        'total_users': "Всього користувачів: {}",
        'total_hours': "Всього зареєстровано годин: {:.2f}",
        'average_hours': "Середня кількість годин на користувача: {:.2f}",
        'top_users': "Топ-{} користувачів за годинами:",
        'user_hours': "{} - {:.2f} годин",
        'no_users': "У базі даних немає користувачів.",
        'no_pending_hours': "Немає годин, що очікують підтвердження.",
        'cannot_confirm_own': "Ви не можете підтвердити свої власні години.",
        'hours_confirmed_admin': "Години підтверджені для користувача ID:{}, у нього тепер {} годин і {} хвилин.",
        'hours_rejected_admin': "Години відхилені для користувача ID:{}."
    }
}

# Default language
DEFAULT_LANGUAGE = 'en'

def get_message(message_key, lang_code='en'):
    """
    Get message by key and language
    
    Args:
        message_key (str): Message key
        lang_code (str): Language code 
        
    Returns:
        str: Message text
    """
    # Get language or fallback to English
    language = lang_code if lang_code in MESSAGES else DEFAULT_LANGUAGE
    
    # Get message or fallback to English message
    if message_key not in MESSAGES[language]:
        return MESSAGES[DEFAULT_LANGUAGE].get(message_key, f"Message not found: {message_key}")
    
    return MESSAGES[language][message_key]