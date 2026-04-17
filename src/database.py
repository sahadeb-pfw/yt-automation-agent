import sqlite3
import json
from datetime import datetime
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    """Database management for storing agent data"""
    
    def __init__(self, db_path: str = "youtube_agent.db"):
        self.db_path = db_path
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize database tables"""
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Articles table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    summary TEXT,
                    link TEXT UNIQUE,
                    published DATE,
                    source TEXT,
                    verified BOOLEAN,
                    verification_score REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Generated content table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS generated_content (
                    id INTEGER PRIMARY KEY,
                    article_id INTEGER,
                    seo_title TEXT,
                    script TEXT,
                    description TEXT,
                    hashtags TEXT,
                    thumbnail_prompt TEXT,
                    generated_at TIMESTAMP,
                    FOREIGN KEY (article_id) REFERENCES articles(id)
                )
            ''')
            
            # Scheduled videos table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS scheduled_videos (
                    id INTEGER PRIMARY KEY,
                    content_id INTEGER,
                    video_id TEXT,
                    title TEXT,
                    scheduled_time TIMESTAMP,
                    posted_time TIMESTAMP,
                    status TEXT DEFAULT 'scheduled',
                    views INTEGER DEFAULT 0,
                    likes INTEGER DEFAULT 0,
                    comments INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (content_id) REFERENCES generated_content(id)
                )
            ''')
            
            # Channel analytics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS channel_analytics (
                    id INTEGER PRIMARY KEY,
                    date DATE,
                    views INTEGER,
                    subscribers INTEGER,
                    watch_time_hours REAL,
                    avg_view_duration REAL,
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("✅ Database initialized successfully")
        
        except Exception as e:
            logger.error(f"❌ Error initializing database: {e}")
    
    def save_article(self, article: Dict) -> int:
        """Save article to database"""
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR IGNORE INTO articles 
                (title, summary, link, published, source, verified, verification_score)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                article.get('title'),
                article.get('summary'),
                article.get('link'),
                article.get('published'),
                article.get('source'),
                article.get('verified'),
                article.get('verification_score', 0)
            ))
            
            conn.commit()
            article_id = cursor.lastrowid
            conn.close()
            
            logger.info(f"✅ Article saved with ID: {article_id}")
            return article_id
        
        except Exception as e:
            logger.error(f"❌ Error saving article: {e}")
            return None
    
    def save_content(self, article_id: int, content_package: Dict) -> int:
        """Save generated content to database"""
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO generated_content
                (article_id, seo_title, script, description, hashtags, thumbnail_prompt, generated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                article_id,
                content_package.get('seo_title'),
                content_package.get('script'),
                content_package.get('description'),
                json.dumps(content_package.get('hashtags', [])),
                content_package.get('thumbnail_prompt'),
                content_package.get('generated_at')
            ))
            
            conn.commit()
            content_id = cursor.lastrowid
            conn.close()
            
            logger.info(f"✅ Content saved with ID: {content_id}")
            return content_id
        
        except Exception as e:
            logger.error(f"❌ Error saving content: {e}")
            return None
    
    def schedule_video(self, content_id: int, title: str, scheduled_time: datetime) -> int:
        """Schedule video for posting"""
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO scheduled_videos
                (content_id, title, scheduled_time, status)
                VALUES (?, ?, ?, 'scheduled')
            ''', (content_id, title, scheduled_time))
            
            conn.commit()
            video_id = cursor.lastrowid
            conn.close()
            
            logger.info(f"✅ Video scheduled with ID: {video_id}")
            return video_id
        
        except Exception as e:
            logger.error(f"❌ Error scheduling video: {e}")
            return None
    
    def update_video_status(self, video_id: int, status: str, posted_time: datetime = None) -> bool:
        """Update video posting status"""
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE scheduled_videos
                SET status = ?, posted_time = ?
                WHERE id = ?
            ''', (status, posted_time, video_id))
            
            conn.commit()
            conn.close()
            
            logger.info(f"✅ Video {video_id} status updated to {status}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Error updating video status: {e}")
            return False
    
    def get_pending_videos(self) -> List[Dict]:
        """Get all pending videos to be posted"""
        
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM scheduled_videos
                WHERE status = 'scheduled' AND scheduled_time <= datetime('now')
                ORDER BY scheduled_time ASC
            ''')
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
        
        except Exception as e:
            logger.error(f"❌ Error fetching pending videos: {e}")
            return []
    
    def record_analytics(self, views: int, subscribers: int, watch_time: float) -> bool:
        """Record channel analytics"""
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO channel_analytics
                (date, views, subscribers, watch_time_hours)
                VALUES (date('now'), ?, ?, ?)
            ''', (views, subscribers, watch_time))
            
            conn.commit()
            conn.close()
            
            logger.info("✅ Analytics recorded")
            return True
        
        except Exception as e:
            logger.error(f"❌ Error recording analytics: {e}")
            return False
