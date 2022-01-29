from .db import DataBase
from dotenv import load_dotenv

load_dotenv()

database_instance = DataBase()