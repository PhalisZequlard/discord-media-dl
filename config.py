import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    APPLICATION_ID = os.getenv('APPLICATION_ID')
    PUBLIC_KEY = os.getenv('PUBLIC_KEY')
    
    # MongoDB settings
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
    MONGODB_DB_NAME = os.getenv('MONGODB_DB_NAME', 'discord_downloader')
    
    # Web GUI settings
    WEB_HOST = "localhost"
    WEB_PORT = 10412
    
    # Allowed user IDs (you can modify this through the web GUI)
    ALLOWED_USERS = set()
    
    # Download settings
    CONCURRENT_DOWNLOADS = 3
    DOWNLOAD_PATH = os.path.join(os.path.dirname(__file__), 'downloads')
    
    # Create download directories if they don't exist
    for dir_name in ['videos', 'music', 'gallery']:
        os.makedirs(os.path.join(DOWNLOAD_PATH, dir_name), exist_ok=True)