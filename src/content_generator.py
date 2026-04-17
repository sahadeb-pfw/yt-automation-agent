import logging
from typing import Dict, List
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentGenerator:
    """Generates video scripts, titles, descriptions, and metadata"""
    
    def __init__(self, openai_api_key: str = ""):
        self.openai_api_key = openai_api_key
    
    def generate_video_script(self, article: Dict, video_duration: int = 300) -> str:
        """Generate engaging video script from news article"""
        
        try:
            logger.info("✍️ Generating video script...")
            
            title = article.get('title', 'Latest News')
            summary = article.get('summary', '')
            
            script = f"""
HOOK (0-3 seconds):
Hey everyone! Breaking news on {title}! You won't believe what just happened.

INTRO (3-10 seconds):
So today we're talking about something really important. This is trending everywhere and you need to know about it.

MAIN CONTENT:
{summary}

This is huge because it affects all of us. Here's what you need to know:
1. The situation
2. Why it matters
3. What comes next

CALL TO ACTION (Last 10 seconds):
If you found this helpful, please:
✓ Like this video
✓ Subscribe for daily news
✓ Hit the notification bell
✓ Comment your thoughts below

Thanks for watching!
"""
            
            logger.info("✅ Script generated successfully")
            return script
        
        except Exception as e:
            logger.error(f"❌ Error generating script: {e}")
            return ""
    
    def generate_seo_title(self, article: Dict, max_length: int = 60) -> str:
        """Generate SEO-optimized YouTube title"""
        
        try:
            logger.info("🎯 Generating SEO title...")
            
            title = article.get('title', 'Breaking News')
            
            if len(title) < max_length:
                seo_title = f"🔥 BREAKING: {title}"
            else:
                seo_title = title[:max_length-3] + "..."
            
            logger.info(f"✅ SEO title: {seo_title}")
            return seo_title[:max_length]
        
        except Exception as e:
            logger.error(f"❌ Error generating title: {e}")
            return article.get('title', '')[:max_length]
    
    def generate_description(self, article: Dict, seo_title: str) -> str:
        """Generate YouTube description"""
        
        try:
            logger.info("📝 Generating description...")
            
            description = f"""
{seo_title}

📺 VIDEO CHAPTERS:
00:00 - Intro
01:00 - What Happened
03:00 - Why It Matters
05:00 - What Comes Next
06:00 - Call to Action

📰 SOURCE:
{article.get('link', 'News Source')}

🔔 SUBSCRIBE for more daily news!
✅ LIKE if you found this helpful
💬 COMMENT your thoughts
🔔 TURN ON NOTIFICATIONS

#News #Breaking #Updates
"""
            
            logger.info("✅ Description generated")
            return description
        
        except Exception as e:
            logger.error(f"❌ Error generating description: {e}")
            return ""
    
    def generate_hashtags(self, article: Dict, count: int = 10) -> List[str]:
        """Generate trending hashtags"""
        
        try:
            logger.info("🏷️ Generating hashtags...")
            
            hashtags = [
                "#BreakingNews",
                "#TrendingNow",
                "#DailyNews",
                "#NewsToday",
                "#Viral",
                "#Latest",
                "#Updates",
                "#Breaking",
                "#NewsUpdate",
                "#MustWatch"
            ]
            
            logger.info(f"✅ Generated {len(hashtags)} hashtags")
            return hashtags[:count]
        
        except Exception as e:
            logger.error(f"❌ Error generating hashtags: {e}")
            return []
    
    def generate_thumbnail_prompt(self, article: Dict) -> str:
        """Generate DALL-E prompt for thumbnail"""
        
        try:
            logger.info("🖼️ Generating thumbnail prompt...")
            
            title = article.get('title', 'Breaking News')
            
            prompt = f"""
Create a YouTube thumbnail for: {title}

Requirements:
- Bold, eye-catching design
- High contrast colors (red, yellow, black)
- Clear, readable text
- 1280x720 resolution
- Shocking or surprising expression
- Professional quality
"""
            
            logger.info("✅ Thumbnail prompt generated")
            return prompt
        
        except Exception as e:
            logger.error(f"❌ Error generating prompt: {e}")
            return ""
    
    def generate_content_package(self, article: Dict) -> Dict:
        """Generate complete content package"""
        
        logger.info(f"📦 Generating content package...")
        
        try:
            seo_title = self.generate_seo_title(article)
            script = self.generate_video_script(article)
            description = self.generate_description(article, seo_title)
            hashtags = self.generate_hashtags(article)
            thumbnail_prompt = self.generate_thumbnail_prompt(article)
            
            content_package = {
                'article': article,
                'seo_title': seo_title,
                'script': script,
                'description': description,
                'hashtags': hashtags,
                'thumbnail_prompt': thumbnail_prompt,
                'generated_at': str(datetime.now())
            }
            
            logger.info("✅ Content package complete")
            return content_package
        
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            return {}
