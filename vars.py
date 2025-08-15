#🇳‌🇮‌🇰‌🇭‌🇮‌🇱‌
# Add your details here and then deploy by clicking on HEROKU Deploy button
import os
from os import environ

API_ID = int(environ.get("API_ID", "21589942"))
API_HASH = environ.get("API_HASH", "f99db4b15e3179c794a058b21b4ad8da")
BOT_TOKEN = environ.get("BOT_TOKEN", "7205844544:AAGfR4-Y_oMPC23o6G-nJJMeNXxSdwOX9dc")

OWNER = int(environ.get("OWNER", "8034639315"))
CREDIT = environ.get("CREDIT", " apka name")

TOTAL_USER = os.environ.get('TOTAL_USERS', '5680454765').split(',')
TOTAL_USERS = [int(user_id) for user_id in TOTAL_USER]

AUTH_USER = os.environ.get('AUTH_USERS', '5680454765').split(',')
AUTH_USERS = [int(user_id) for user_id in AUTH_USER]
if int(OWNER) not in AUTH_USERS:
    AUTH_USERS.append(int(OWNER))
  
#WEBHOOK = True  # Don't change this
#PORT = int(os.environ.get("PORT", 8080))  # Default to 8000 if not set



