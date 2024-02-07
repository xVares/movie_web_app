import os
import logging
from flask import Flask
from dotenv import load_dotenv
from data_manager.sql_data_manager import SQLiteDataManager

# --- Load environment variables ---
load_dotenv()

# --- URLs & URIs for Data and API Access ---
DATABASE_URI = "sqlite:///user_data/movies.sqlite"
JSON_DATA_PATH = "user_data/movie_data.json"
API_KEY = os.environ.get("MY_API_KEY")
FETCH_MOVIE_URL = f"http://www.omdbapi.com/?apikey={API_KEY}"

# --- App Config ---
app = Flask(__name__)
data_manager = SQLiteDataManager(app, DATABASE_URI)

# --- Logger Config ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
