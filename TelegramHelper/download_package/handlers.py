import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime

import config
from database import Database
import keyboards
from languages import get_message

# Initialize router and database
router = Router()
db = Database()
logger = logging.getLogger(__name__)

# Global store for pending requests and user selections
pending_requests = {}  # {user_id: hours}
user_selection = {}    # {user_id: hours}

# Define states for conversation flow
class HourLogging(StatesGroup):
    waiting_for_hours = State()
    waiting_for_minutes = State()
    waiting_for_custom_hours = State()

@router.message(Command("start"))
async def start_command(message: types.Message):
    """Handle /start command"""
    user_id = message.from_user.id
    user = db.get_user(user_id)
    
    if not user:
        # Create new user if not exists
        db.create_user(
            user_id=user_id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            language=message.from_user.language_code or 'en'
        )
        logger.info(f"New user registered: {user_id}")
    
    # Get user's language preference
    lang_code = db.get_user_language(user_id)
    
    # Send welcome message in user's language
    welcome_message = get_message('welcome', lang_code).format(message.from_user.first_name)
    await message.answer(
        welcome_message,
        reply_markup=keyboards.get_client_keyboard(lang_code)
    )

@router.message(F.text.in_(["Log Hours", "Записать часы", "Zapisz godziny", "Записати години"]))
async def request_hours(message: types.Message, state: FSMContext):
    """Handle hour logging request"""
    user_id = message.from_user.id
    lang_code = db.get_user_language(user_id)
    
    await state.set_state(HourLogging.waiting_for_hours)
    await message.answer(
        get_message('select_hours', lang_code),
        reply_markup=keyboards.get_hour_keyboard()
    )

@router.message(F.text.in_(["Check Hours", "Проверить часы", "Sprawdź godziny", "Перевірити години"]))
async def check_hours(message: types.Message):
    """Show user's current hours"""
    user_id = message.from_user.id
    lang_code = db.get_user_language(user_id)
    hours = db.get_user_hours(user_id)
    
    # Calculate full hours and remaining minutes
    full_hours = int(hours)
    minutes = int((hours - full_hours) * 60)
    
    # Calculate free hours based on configuration
    free_hours = int(hours // config.HOURS_FOR_FREE_SESSION)
    remaining_for_next = hours % config.HOURS_FOR_FREE_SESSION
    
    # Build the response using localized messages
    current_hours_msg = get_message('current_hours', lang_code).format(full_hours, minutes)
    response = current_hours_msg
    
    if free_hours > 0:
        free_sessions_msg = get_message('free_sessions', lang_code).format(free_hours)
        response += free_sessions_msg
    
    # Format the hours needed for next session more cleanly with 1 decimal place
    hours_needed = config.HOURS_FOR_FREE_SESSION - remaining_for_next
    next_free_msg = get_message('next_free_session', lang_code).format(
        f"{hours_needed:.1f}"
    )
    response += next_free_msg
    
    await message.answer(response, reply_markup=keyboards.get_client_keyboard(lang_code))

@router.message(HourLogging.waiting_for_hours, F.text.isdigit())
async def process_hours(message: types.Message, state: FSMContext):
    """Handle hour selection"""
    user_id = message.from_user.id
    lang_code = db.get_user_language(user_id)
    hours = int(message.text)
    
    # Save hour selection
    user_selection[user_id] = float(hours)
    await state.set_state(HourLogging.waiting_for_minutes)
    
    await message.answer(
        get_message('select_minutes', lang_code), 
        reply_markup=keyboards.get_minute_keyboard()
    )

@router.message(HourLogging.waiting_for_hours, F.text == "More")
async def request_custom_hours(message: types.Message, state: FSMContext):
    """Handle custom hour input request"""
    user_id = message.from_user.id
    lang_code = db.get_user_language(user_id)
    
    await state.set_state(HourLogging.waiting_for_custom_hours)
    await message.answer(get_message('custom_hours_prompt', lang_code))

@router.message(HourLogging.waiting_for_custom_hours)
async def process_custom_hours(message: types.Message, state: FSMContext):
    """Process custom hour input"""
    user_id = message.from_user.id
    lang_code = db.get_user_language(user_id)
    
    try:
        hours = float(message.text.replace(',', '.'))
        
        if hours <= 0:
            await message.answer(get_message('non_positive_number', lang_code))
            return
            
        # Process the hours directly without minute selection
        pending_requests[user_id] = hours
        
        # Log the hours in database
        log_id = db.log_hours(user_id, hours)
        
        # Notify admins
        for admin_id in config.ADMIN_IDS:
            try:
                await message.bot.send_message(
                    admin_id,
                    f"User @{message.from_user.username or f'ID:{user_id}'} logged {hours} hours. Confirm?",
                    reply_markup=keyboards.get_admin_confirmation_keyboard()
                )
            except Exception as e:
                logger.error(f"Failed to notify admin {admin_id}: {e}")
        
        await message.answer(
            get_message('hours_sent', lang_code),
            reply_markup=keyboards.get_client_keyboard(lang_code)
        )
        await state.clear()
        
    except ValueError:
        await message.answer(get_message('invalid_number', lang_code))

@router.message(HourLogging.waiting_for_minutes, F.text.in_(["0 minutes", "15 minutes", "30 minutes", "45 minutes"]))
async def process_minutes(message: types.Message, state: FSMContext):
    """Handle minute selection"""
    user_id = message.from_user.id
    lang_code = db.get_user_language(user_id)
    
    # Convert minutes to decimal hours
    minute_values = {
        "0 minutes": 0, 
        "15 minutes": 0.25, 
        "30 minutes": 0.5, 
        "45 minutes": 0.75
    }
    minutes = minute_values[message.text]
    
    # Calculate total hours
    total_hours = user_selection.get(user_id, 0) + minutes
    pending_requests[user_id] = total_hours
    
    # Log the hours in database
    log_id = db.log_hours(user_id, total_hours)
    
    # Notify admins
    for admin_id in config.ADMIN_IDS:
        try:
            await message.bot.send_message(
                admin_id,
                f"User @{message.from_user.username or f'ID:{user_id}'} logged {total_hours} hours. Confirm?",
                reply_markup=keyboards.get_admin_confirmation_keyboard()
            )
        except Exception as e:
            logger.error(f"Failed to notify admin {admin_id}: {e}")
    
    await message.answer(
        get_message('hours_sent', lang_code),
        reply_markup=keyboards.get_client_keyboard(lang_code)
    )
    await state.clear()

@router.message(F.text.in_(["✅ Confirm", "❌ Reject"]))
async def admin_confirm_hours(message: types.Message):
    """Handle admin confirmation of hours"""
    admin_id = message.from_user.id
    
    # Verify sender is an admin
    if admin_id not in config.ADMIN_IDS:
        logger.warning(f"Non-admin user {admin_id} attempted to confirm hours")
        return
    
    # Check if there are pending requests
    if not pending_requests:
        lang_code = db.get_user_language(admin_id)
        await message.answer(
            get_message('no_pending_hours', lang_code),
            reply_markup=keyboards.get_client_keyboard(lang_code)
        )
        return
    
    # Get the first pending request
    user_id, hours = pending_requests.popitem()
    user_lang = db.get_user_language(user_id)
    
    # Admin can't confirm their own hours
    if user_id == admin_id:
        pending_requests[user_id] = hours  # Put it back into the queue
        lang_code = db.get_user_language(admin_id)
        await message.answer(
            get_message('cannot_confirm_own', lang_code),
            reply_markup=keyboards.get_client_keyboard(lang_code)
        )
        return
    
    if message.text == "✅ Confirm":
        # Get current hours from database
        current_hours = db.get_user_hours(user_id)
        new_hours = current_hours + hours
        
        # Calculate free hours and remaining hours
        free_hours = int(new_hours // config.HOURS_FOR_FREE_SESSION)
        remaining_hours = new_hours % config.HOURS_FOR_FREE_SESSION
        
        # Update the database with remaining hours
        db.update_hours(user_id, remaining_hours)
        
        # Format hours and minutes for display
        full_hours = int(remaining_hours)
        minutes = int((remaining_hours - full_hours) * 60)
        
        # Unfortunately we don't have the log_id here since we're using a simple pending_requests dict
        # In a real app we'd need to store the log_id with the request
        
        # Send confirmation to user
        try:
            confirmation_msg = get_message('hours_confirmed', user_lang).format(
                free_hours, full_hours, minutes
            )
            await message.bot.send_message(
                user_id,
                confirmation_msg,
                reply_markup=keyboards.get_client_keyboard(user_lang)
            )
        except Exception as e:
            logger.error(f"Failed to notify user {user_id} of confirmation: {e}")
            
        # Format the admin confirmation message
        full_hours = int(remaining_hours)
        minutes = int((remaining_hours - full_hours) * 60)
        lang_code = db.get_user_language(admin_id)
        await message.answer(
            get_message('hours_confirmed_admin', lang_code).format(
                user_id, full_hours, minutes
            ),
            reply_markup=keyboards.get_client_keyboard(lang_code)
        )
        
    else:  # Reject hours
        try:
            rejection_msg = get_message('hours_rejected', user_lang)
            await message.bot.send_message(
                user_id,
                rejection_msg,
                reply_markup=keyboards.get_client_keyboard(user_lang)
            )
        except Exception as e:
            logger.error(f"Failed to notify user {user_id} of rejection: {e}")
            
        # Send formatted rejection confirmation to admin
        lang_code = db.get_user_language(admin_id)
        await message.answer(
            get_message('hours_rejected_admin', lang_code).format(user_id),
            reply_markup=keyboards.get_client_keyboard(lang_code)
        )

@router.message(F.text.in_(["Language 🌐", "Язык 🌐", "Język 🌐", "Мова 🌐"]))
async def language_command(message: types.Message):
    """Handle language selection request"""
    user_id = message.from_user.id
    lang_code = db.get_user_language(user_id)
    
    await message.answer(
        get_message('choose_language', lang_code),
        reply_markup=keyboards.get_language_keyboard()
    )

@router.callback_query(F.data.startswith("lang_"))
async def process_language_callback(callback_query: types.CallbackQuery):
    """Handle language selection callback"""
    user_id = callback_query.from_user.id
    new_lang = callback_query.data.split("_")[1]
    
    # Update user language in database
    db.update_user_language(user_id, new_lang)
    
    # Send confirmation
    await callback_query.message.edit_text(
        get_message('language_changed', new_lang)
    )
    
    # Send updated main menu
    await callback_query.message.answer(
        get_message('welcome', new_lang).format(callback_query.from_user.first_name),
        reply_markup=keyboards.get_client_keyboard(new_lang)
    )
    
    # Answer callback to stop loading animation
    await callback_query.answer()

@router.message(F.text.in_(["History", "История", "Historia", "Історія"]))
async def history_command(message: types.Message):
    """Show user's hour log history"""
    user_id = message.from_user.id
    lang_code = db.get_user_language(user_id)
    
    # Get user's hour logs
    logs = db.get_user_hour_logs(user_id)
    
    if not logs:
        await message.answer(
            get_message('no_logs', lang_code),
            reply_markup=keyboards.get_client_keyboard(lang_code)
        )
        return
    
    # Format and display logs
    response = get_message('history_header', lang_code) + "\n\n"
    
    # Translations for status
    confirmed_text = get_message('status_confirmed', lang_code)
    pending_text = get_message('status_pending', lang_code)
    
    for log in logs:
        date = datetime.datetime.strptime(log["created_at"], "%Y-%m-%d %H:%M:%S")
        status = confirmed_text if log["confirmed"] else pending_text
        hours_text = get_message('hours_text', lang_code).format(log['hours'])
        
        response += f"{date.strftime('%d %b %Y, %H:%M')}: {hours_text} - {status}\n"
    
    await message.answer(
        response,
        reply_markup=keyboards.get_client_keyboard(lang_code)
    )

@router.message(Command("stats"))
async def stats_command(message: types.Message):
    """Show statistics for admins"""
    user_id = message.from_user.id
    lang_code = db.get_user_language(user_id)
    
    # Only admins can access statistics
    if user_id not in config.ADMIN_IDS:
        return
    
    # Get all users
    users = db.get_all_users()
    
    if not users:
        await message.answer(
            get_message('no_users', lang_code),
            reply_markup=keyboards.get_client_keyboard(lang_code)
        )
        return
    
    total_hours = sum(user["hours"] for user in users)
    average_hours = total_hours / len(users) if users else 0
    top_count = 5
    
    response = get_message('stats_header', lang_code) + "\n\n"
    response += get_message('total_users', lang_code).format(len(users)) + "\n"
    response += get_message('total_hours', lang_code).format(total_hours) + "\n"
    response += get_message('average_hours', lang_code).format(average_hours) + "\n\n"
    response += get_message('top_users', lang_code).format(top_count) + "\n"
    
    # Add top 5 users
    for i, user in enumerate(users[:top_count], 1):
        response += f"{i}. "
        user_display = ""
        if user["username"]:
            user_display = f"@{user['username']}"
        else:
            user_display = f"{user['first_name'] or ''} {user['last_name'] or ''}".strip()
            if not user_display:
                user_display = f"ID:{user['user_id']}"
        
        response += get_message('user_hours', lang_code).format(user_display, user['hours']) + "\n"
    
    await message.answer(response, reply_markup=keyboards.get_client_keyboard(lang_code))
