"""Configuration for the Slack integration"""

import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
BOT_USER_OAUTH_TOKEN = os.getenv("BOT_USER_OAUTH_TOKEN")
