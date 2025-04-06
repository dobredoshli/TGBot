import asyncio
from aiogram import Bot
import config

async def delete_webhook():
    """Delete the Telegram bot webhook"""
    bot = Bot(token=config.TOKEN)
    result = await bot.delete_webhook(drop_pending_updates=True)
    print(f"Webhook deleted: {result}")
    await bot.session.close()

if __name__ == "__main__":
    asyncio.run(delete_webhook())