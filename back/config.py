import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_USER = os.getenv("DEFAULT_USER", "user1")
