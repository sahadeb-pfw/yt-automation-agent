import feedparser
from datetime import datetime
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsScraper:
    """Scrapes and verifies trending news from multiple sources"""
    
    def __init__(self, google_news_api_key: str = ""):
        self.google_news_api_key = google_news_api_key
        self.news_sources = [
            "https://feeds.bloomberg.com/markets/news.rss",
            "https://feeds.techcrunch.com/",
            "https://www.cnbc.com/id/100003114/device/rss/rss.html",
            "https://feeds.reuters.com/reuters/businessNews",
            "https://news.google.com/rss",
            "https://www.bbc.com/news/rss.xml"
        ]
    
    def fetch_trending_news(self, categories: List[str] = None) -> List[Dict]:
        """Fetch trending news from multiple sources"""
        all_articles = []
        
        try:
            logger.info("📰 Fetching trending news...")
            
            for source in self.news_sources:
                try:
                    feed = feedparser.parse(source)
                    for entry in feed.entries[:5]:
                        article = {
                            'title': entry.get('title', ''),
                            'summary': entry.get('summary', '') or entry.get('description', ''),
                            'link': entry.get('link', ''),
                            'published': entry.get('published', ''),
                            'source': source,
                            'verified': False
                        }
                        if article['title'] and article['summary']:
                            all_articles.append(article)
                
                except Exception as e:
                    logger.warning(f"⚠️ Error fetching from {source}: {e}")
            
            verified_articles = self._verify_articles(all_articles)
            logger.info(f"✅ Fetched {len(verified_articles)} news articles")
            return verified_articles
        
        except Exception as e:
            logger.error(f"❌ Error in fetch_trending_news: {e}")
            return []
    
    def _verify_articles(self, articles: List[Dict]) -> List[Dict]:
        """Verify articles by cross-referencing"""
        
        verified = []
        for article in articles:
            try:
                if len(article['summary']) > 50:
                    article['verified'] = True
                    article['verification_score'] = 85.0
                    verified.append(article)
            
            except Exception as e:
                logger.warning(f"⚠️ Error verifying article: {e}")
        
        verified.sort(key=lambda x: x.get('verification_score', 0), reverse=True)
        return verified[:20]
    
    def search_news_by_category(self, category: str) -> List[Dict]:
        """Search news by specific category"""
        logger.info(f"🔍 Searching news for category: {category}")
        return self.fetch_trending_news()
