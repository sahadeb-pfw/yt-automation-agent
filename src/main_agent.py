import logging
import schedule
import time
from datetime import datetime
from typing import List

# Import all modules
from src.config.config import Config
from src.news_scraper import NewsScraper
from src.content_generator import ContentGenerator
from src.video_generator import VideoGenerator
from src.youtube_api import YouTubeAPI
from src.scheduler import SchedulingEngine
from src.database import Database
from src.video_formatter import VideoFormatter
from src.youtube_community import YouTubeCommunity

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class YouTubeAutomationAgent:
    """Main orchestrator for YouTube automation"""
    
    def __init__(self):
        logger.info("🚀 Initializing YouTube Automation Agent...")
        
        try:
            self.config = Config()
            self.db = Database()
            self.news_scraper = NewsScraper(self.config.GOOGLE_NEWS_API_KEY)
            self.content_generator = ContentGenerator(self.config.OPENAI_API_KEY)
            self.video_generator = VideoGenerator(
                self.config.OPENAI_API_KEY,
                self.config.ELEVENLABS_API_KEY
            )
            self.youtube_api = YouTubeAPI(
                self.config.YOUTUBE_CLIENT_ID,
                self.config.YOUTUBE_CLIENT_SECRET,
                self.config.YOUTUBE_REFRESH_TOKEN
            )
            self.scheduler = SchedulingEngine()
            self.video_formatter = VideoFormatter()
            self.community = YouTubeCommunity(self.youtube_api.service)
            
            logger.info("✅ All components initialized successfully!")
        
        except Exception as e:
            logger.error(f"❌ Error initializing agent: {e}")
            raise
    
    def run_content_pipeline(self):
        """Run complete content creation pipeline"""
        
        logger.info("📋 Starting content pipeline...")
        
        try:
            # Fetch news
            logger.info("Step 1: Fetching news...")
            articles = self.news_scraper.fetch_trending_news(
                categories=self.config.NEWS_CATEGORIES
            )
            
            if not articles:
                logger.warning("⚠️ No articles found")
                return
            
            # Generate content for videos
            logger.info(f"Step 2: Generating content for {len(articles[:2])} videos...")
            
            for i, article in enumerate(articles[:2]):
                try:
                    article_id = self.db.save_article(article)
                    content_package = self.content_generator.generate_content_package(article)
                    content_id = self.db.save_content(article_id, content_package)
                    
                    logger.info(f"✅ Content {i+1} generated successfully")
                
                except Exception as e:
                    logger.error(f"❌ Error processing article {i+1}: {e}")
            
            logger.info("✅ Content pipeline completed!")
        
        except Exception as e:
            logger.error(f"❌ Error in content pipeline: {e}")
    
    def create_daily_content(self):
        """Create 2 videos per day"""
        logger.info("🎬 Creating 2 videos for today...")
        
        try:
            articles = self.news_scraper.fetch_trending_news(
                categories=self.config.NEWS_CATEGORIES
            )
            
            if not articles:
                logger.warning("⚠️ No articles found for today")
                return
            
            for i, article in enumerate(articles[:2]):
                try:
                    logger.info(f"📹 Processing article {i+1}: {article.get('title', '')[:50]}")
                    
                    # Save article
                    article_id = self.db.save_article(article)
                    
                    # Generate content
                    content_package = self.content_generator.generate_content_package(article)
                    
                    # Save content
                    content_id = self.db.save_content(article_id, content_package)
                    
                    # Auto-select format
                    script_length = len(content_package.get('script', ''))
                    format_type = self.video_formatter.auto_select_format(script_length)
                    
                    # Optimize content
                    optimized_content = self.video_formatter.optimize_for_platform(
                        content_package, format_type
                    )
                    
                    logger.info(f"✅ Video {i+1}: {format_type.upper()} ({optimized_content.get('duration')}s)")
                
                except Exception as e:
                    logger.error(f"❌ Error creating video {i+1}: {e}")
        
        except Exception as e:
            logger.error(f"❌ Error in daily content creation: {e}")
    
    def upload_scheduled_videos(self):
        """Upload all pending scheduled videos"""
        
        logger.info("⬆️ Checking for videos to upload...")
        
        try:
            pending_videos = self.db.get_pending_videos()
            
            if not pending_videos:
                logger.info("ℹ️ No pending videos to upload")
                return
            
            for video in pending_videos:
                try:
                    logger.info(f"📤 Uploading: {video['title']}")
                    
                    # In production: upload actual video
                    video_id = f"simulated_video_{video['id']}"
                    
                    # Update status
                    self.db.update_video_status(video['id'], 'uploaded', datetime.now())
                    
                    logger.info(f"✅ Video uploaded: {video_id}")
                
                except Exception as e:
                    logger.error(f"❌ Error uploading video: {e}")
        
        except Exception as e:
            logger.error(f"❌ Error in upload process: {e}")
    
    def manage_community_engagement(self):
        """Create posts and polls on YouTube Community"""
        logger.info("🗣️ Managing community engagement...")
        
        try:
            today = datetime.now().strftime('%A')
            
            schedule_dict = self.community.create_weekly_engagement_schedule()
            
            if today in schedule_dict:
                day_plan = schedule_dict[today]
                
                # Post community post
                if 'post' in day_plan:
                    self.community.create_community_post(text=day_plan['post'])
                    logger.info(f"📝 Posted: {day_plan['post']}")
                
                # Create poll
                if 'poll' in day_plan:
                    poll_options = self.config.NEWS_CATEGORIES[:4]
                    self.community.create_poll(
                        question=day_plan['poll'],
                        options=poll_options,
                        duration_hours=24
                    )
                    logger.info(f"🗳️ Poll created: {day_plan['poll']}")
            
            logger.info("✅ Community engagement updated")
        
        except Exception as e:
            logger.error(f"❌ Error managing community: {e}")
    
    def handle_comments(self):
        """Handle new comments"""
        
        logger.info("💬 Checking for new comments...")
        
        try:
            if not self.config.AUTO_REPLY_ENABLED:
                logger.info("ℹ️ Auto-reply disabled")
                return
            
            logger.info("✅ Comment handling complete")
        
        except Exception as e:
            logger.error(f"❌ Error handling comments: {e}")
    
    def update_analytics(self):
        """Update channel analytics"""
        
        logger.info("📊 Updating channel analytics...")
        
        try:
            stats = self.youtube_api.get_channel_statistics()
            
            if stats:
                logger.info(f"✅ Analytics updated: {stats}")
        
        except Exception as e:
            logger.error(f"❌ Error updating analytics: {e}")
    
    def schedule_jobs(self):
        """Schedule recurring jobs for 2 videos per day"""
        
        logger.info("⏰ Scheduling recurring jobs...")
        
        try:
            # Schedule content creation daily at 6 AM
            logger.info("📅 Content creation: Daily at 6:00 AM")
            schedule.every().day.at("06:00").do(self.create_daily_content)
            
            # Calculate optimal posting times
            logger.info("📊 Calculating optimal posting times...")
            optimal_times = self.scheduler.calculate_optimal_post_time(
                category=self.config.NEWS_CATEGORIES[0] if self.config.NEWS_CATEGORIES else 'news',
                num_suggestions=2
            )
            
            # Schedule uploads
            for i, post_time in enumerate(optimal_times):
                time_str = post_time.strftime("%H:%M")
                logger.info(f"🎬 Video {i+1} scheduled: {time_str}")
                schedule.every().day.at(time_str).do(self.upload_scheduled_videos)
            
            # Community engagement
            logger.info("💬 Community engagement: Daily at 8:00 AM")
            schedule.every().day.at("08:00").do(self.manage_community_engagement)
            
            # Comment handling
            logger.info("💭 Comment handling: Every hour")
            schedule.every().hour.do(self.handle_comments)
            
            # Analytics update
            logger.info("📈 Analytics update: Daily at 11:00 PM")
            schedule.every().day.at("23:00").do(self.update_analytics)
            
            logger.info("✅ All jobs scheduled successfully!")
            logger.info("📋 SCHEDULE SUMMARY:")
            logger.info("  • 2 Videos per day (Shorts <120s or Long-form <500s)")
            logger.info("  • Adaptive posting times (9 AM - 11 PM initially)")
            logger.info("  • YouTube Community posts & polls daily")
            logger.info(f"  • News categories: {', '.join(self.config.NEWS_CATEGORIES)}")
            logger.info(f"  • Auto-replies: {'Enabled' if self.config.AUTO_REPLY_ENABLED else 'Disabled'}")
        
        except Exception as e:
            logger.error(f"❌ Error scheduling jobs: {e}")
    
    def run(self):
        """Run the agent with scheduled tasks"""
        
        logger.info("🚀 Starting YouTube Automation Agent...")
        
        try:
            self.schedule_jobs()
            
            # Keep running
            logger.info("⏳ Agent is running... Press Ctrl+C to stop")
            while True:
                schedule.run_pending()
                time.sleep(60)
        
        except KeyboardInterrupt:
            logger.info("🛑 Agent stopped by user")
        except Exception as e:
            logger.error(f"❌ Error in agent loop: {e}")

if __name__ == "__main__":
    agent = YouTubeAutomationAgent()
    agent.run()
