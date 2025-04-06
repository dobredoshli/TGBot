import os
import logging

# Bot configuration
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "7743710220:AAEKNuBz6kN0vMs-bd_zIfUKcknF47rwfUo")
ADMIN_IDS = [int(admin_id) for admin_id in os.environ.get("ADMIN_IDS", "5791051959").split(",")]

# Database configuration
DB_PATH = os.path.join(os.path.dirname(__file__), 'loyalty.db')

# Hour conversion settings
HOURS_FOR_FREE_SESSION = 8

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
