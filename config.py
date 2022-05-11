# config.py
import os

host = os.environ.get("HOST", default="db")
database = os.environ.get("DATABASE", default="flask_db")
user = os.environ.get("DB_USER", default="user")
password = os.environ.get("DB_PASS", default="pass")
