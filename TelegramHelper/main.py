import asyncio
import logging
import os
import sys
import traceback
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.exceptions import TelegramAPIError

import config
from handlers import router
from database import Database

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

async def setup_database():
    """Set up the database with required tables"""
    try:
        db = Database()
        db.create_tables()
        db.close()
        logger.info("Database setup completed successfully")
    except Exception as e:
        logger.error(f"Error setting up database: {e}")
        traceback.print_exc()
        raise

async def main():
    """Main function to run the bot"""
    try:
        # Initialize database
        await setup_database()
        
        # Initialize bot and dispatcher
        bot = Bot(token=config.TOKEN)
        
        # Delete webhook before starting polling
        await bot.delete_webhook(drop_pending_updates=True)
        
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)
        
        # Register handlers
        dp.include_router(router)
        
        # Log startup information
        logger.info(f"Starting @{(await bot.get_me()).username} bot...")
        
        # Start polling
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except TelegramAPIError as e:
        logger.error(f"Telegram API Error: {e}")
        traceback.print_exc()
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        traceback.print_exc()
    finally:
        # Close database connection when bot stops
        try:
            db = Database()
            db.close()
        except Exception as e:
            logger.error(f"Error closing database: {e}")
        
        logger.info("Bot stopped")

if __name__ == "__main__":
    try:
        # Run the main function
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Unhandled error: {e}")
