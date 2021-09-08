import os

from flask_login.config import USE_SESSION_FOR_NEXT

BOT_TOKEN = os.environ["BOT_TOKEN"]
SECRET_KEY = os.environ["SECRET_KEY"]
#USE_SESSION_FOR_NEXT = True


__all__ = ["BOT_TOKEN", "SECRET_KEY", "USE_SESSION_FOR_NEXT"]
