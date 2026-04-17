import logging
from typing import Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoFormatter:
    """Formats content for Shorts (120s) or Long-form (500s)"""
    
    SHORTS_DURATION = 120  # seconds
    LONGFORM_DURATION = 500  # seconds
    
    def __init__(self):
        self.format_type = None
    
    def auto_select_format(self, script_length: int) -> str:
        """Auto-select format based on script length
        
        Args:
            script_length: Length of script in characters
        
        Returns:
            'shorts' or 'longform'
        """
        # Rough estimate: ~130 characters per second of speech
        estimated_duration = script_length / 130
        
        if estimated_duration < 120:
            return 'shorts'
        else:
            return 'longform'
    
    def format_for_shorts(self, script: str) -> str:
        """Adapt script for YouTube Shorts (< 120 seconds)
        
        Strategy:
        - Hook (2-3 sec): Grab attention immediately
        - Main content (100 sec): Quick facts, visuals
        - CTA (5-10 sec): Subscribe, like, share
        """
        logger.info("⏱️ Formatting script for Shorts (120s max)")
        
        try:
            # Estimate: ~130 characters = 1 second
            # 120 seconds = ~15,600 characters max
            max_chars = 120 * 130
            
            if len(script) > max_chars:
                # Truncate to fit
                words = script.split()
                shorts_words = words[:int(max_chars / 5)]  # Rough estimate
                shorts_text = ' '.join(shorts_words)
            else:
                shorts_text = script
            
            logger.info(f"✅ Shorts script ready: {len(shorts_text)} chars (~{len(shorts_text)//130}s)")
            return shorts_text
        
        except Exception as e:
            logger.error(f"Error formatting for shorts: {e}")
            return script[:15600]  # Fallback: truncate to 120s worth
    
    def format_for_longform(self, script: str) -> str:
        """Adapt script for long-form videos (< 500 seconds)
        
        Strategy:
        - Introduction (10-20s): Context and hook
        - Main content (400s): Detailed explanation
        - Call-to-action (20-30s): Encourage engagement
        """
        logger.info("📺 Formatting script for Long-form (500s max)")
        
        try:
            # 500 seconds = ~65,000 characters max
            max_chars = 500 * 130
            
            if len(script) > max_chars:
                words = script.split()
                longform_words = words[:int(max_chars / 5)]
                longform_text = ' '.join(longform_words)
            else:
                longform_text = script
            
            logger.info(f"✅ Long-form script ready: {len(longform_text)} chars (~{len(longform_text)//130}s)")
            return longform_text
        
        except Exception as e:
            logger.error(f"Error formatting for longform: {e}")
            return script
    
    def generate_format_specific_script(self, content: Dict, format_type: str) -> str:
        """Generate script optimized for specific format
        
        Args:
            content: Content dictionary with 'script' key
            format_type: 'shorts' or 'longform'
        
        Returns:
            Formatted script
        """
        
        try:
            script = content.get('script', '')
            
            if format_type == 'shorts':
                logger.info("📊 Applying Shorts optimization...")
                formatted_script = self.format_for_shorts(script)
            
            elif format_type == 'longform':
                logger.info("📊 Applying Long-form optimization...")
                formatted_script = self.format_for_longform(script)
            
            else:
                logger.warning(f"Unknown format: {format_type}, using original script")
                formatted_script = script
            
            return formatted_script
        
        except Exception as e:
            logger.error(f"Error generating format-specific script: {e}")
            return content.get('script', '')
    
    def get_voiceover_speed(self, format_type: str) -> float:
        """Get recommended voiceover speed for format
        
        Args:
            format_type: 'shorts' or 'longform'
        
        Returns:
            Speed multiplier (1.0 = normal speed)
        """
        if format_type == 'shorts':
            return 1.2  # Faster pacing for shorts
        else:
            return 1.0  # Normal speed for long-form
    
    def get_background_music_duration(self, format_type: str) -> int:
        """Get music duration needed for format (in seconds)
        
        Args:
            format_type: 'shorts' or 'longform'
        
        Returns:
            Duration in seconds
        """
        if format_type == 'shorts':
            return self.SHORTS_DURATION  # 120 seconds
        else:
            return self.LONGFORM_DURATION  # 500 seconds
    
    def get_recommended_fps(self, format_type: str) -> int:
        """Get recommended FPS (frames per second) for format
        
        Args:
            format_type: 'shorts' or 'longform'
        
        Returns:
            FPS value
        """
        if format_type == 'shorts':
            return 30  # Standard 30fps for shorts
        else:
            return 60  # Higher quality 60fps for long-form
    
    def get_thumbnail_orientation(self, format_type: str) -> str:
        """Get recommended thumbnail orientation
        
        Args:
            format_type: 'shorts' or 'longform'
        
        Returns:
            'vertical' or 'horizontal'
        """
        if format_type == 'shorts':
            return 'vertical'  # 9:16 aspect ratio
        else:
            return 'horizontal'  # 16:9 aspect ratio
    
    def add_shorts_effects(self, script: Dict) -> Dict:
        """Add Shorts-specific formatting effects
        
        Args:
            script: Script dictionary
        
        Returns:
            Script with Shorts effects
        """
        try:
            logger.info("✨ Adding Shorts visual effects...")
            
            shorts_enhanced = script.copy()
            
            # Add Shorts-specific metadata
            shorts_enhanced['effects'] = {
                'transitions': 'fast',
                'music_beat_sync': True,
                'text_animations': True,
                'zoom_effect': 'enabled',
                'trending_sounds': True
            }
            
            shorts_enhanced['pacing'] = 'fast'
            shorts_enhanced['visual_cuts_per_minute'] = 4  # More cuts for shorts
            
            logger.info("✅ Shorts effects applied")
            return shorts_enhanced
        
        except Exception as e:
            logger.error(f"Error adding Shorts effects: {e}")
            return script
    
    def add_longform_structure(self, script: Dict) -> Dict:
        """Add Long-form specific structure
        
        Args:
            script: Script dictionary
        
        Returns:
            Script with Long-form structure
        """
        try:
            logger.info("📐 Adding Long-form structure...")
            
            longform_enhanced = script.copy()
            
            # Add Long-form specific metadata
            longform_enhanced['structure'] = {
                'intro_duration': 15,
                'main_content_duration': 400,
                'outro_duration': 25,
                'chapter_markers': True,
                'timestamps': True
            }
            
            longform_enhanced['pacing'] = 'moderate'
            longform_enhanced['visual_cuts_per_minute'] = 2  # Fewer cuts for long-form
            
            logger.info("✅ Long-form structure applied")
            return longform_enhanced
        
        except Exception as e:
            logger.error(f"Error adding Long-form structure: {e}")
            return script
    
    def optimize_for_platform(self, content: Dict, format_type: str) -> Dict:
        """Optimize content for specific YouTube format
        
        Args:
            content: Content dictionary
            format_type: 'shorts' or 'longform'
        
        Returns:
            Platform-optimized content
        """
        try:
            logger.info(f"🎬 Optimizing for {format_type.upper()}...")
            
            optimized = content.copy()
            
            # Apply format-specific optimizations
            if format_type == 'shorts':
                optimized = self.add_shorts_effects(optimized)
            else:
                optimized = self.add_longform_structure(optimized)
            
            # Add metadata
            optimized['format'] = format_type
            optimized['duration'] = self.get_background_music_duration(format_type)
            optimized['fps'] = self.get_recommended_fps(format_type)
            optimized['voiceover_speed'] = self.get_voiceover_speed(format_type)
            
            logger.info(f"✅ Content optimized for {format_type}")
            return optimized
        
        except Exception as e:
            logger.error(f"Error optimizing for platform: {e}")
            return content
