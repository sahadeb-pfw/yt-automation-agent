import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration settings for the YouTube AI Agent"""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
    GOOGLE_NEWS_API_KEY = os.getenv("GOOGLE_NEWS_API_KEY", "")
    
    # YouTube API
    YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID", "")
    YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET", "")
    YOUTUBE_REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN", "")
    
    # Agent Settings
    VIDEOS_PER_DAY = int(os.getenv("VIDEOS_PER_DAY", 2))
    POST_TIME = os.getenv("POST_TIME", "09:00,11:00,14:00,18:00,20:00,23:00")
    VIDEO_FORMAT = os.getenv("VIDEO_FORMAT", "both")
    NEWS_CATEGORIES = os.getenv("NEWS_CATEGORIES", "ai,technology,sports,entertainment,news,business,science").split(",")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///youtube_agent.db")
    
    # Auto-reply settings
    AUTO_REPLY_ENABLED = os.getenv("AUTO_REPLY_ENABLED", "false").lower() == "true"
    
    # Content Settings
    CONTENT_LANGUAGE = os.getenv("CONTENT_LANGUAGE", "en")
    THUMBNAIL_SIZE = (1280, 720)
    VIDEO_QUALITY = "1080p"
    SHORTS_MAX_DURATION = int(os.getenv("SHORTS_MAX_DURATION", 120))
    LONGFORM_MAX_DURATION = int(os.getenv("LONGFORM_MAX_DURATION", 500))
