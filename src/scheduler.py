from datetime import datetime, timedelta
import logging
from typing import List, Tuple, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SchedulingEngine:
    """Calculates optimal posting times with adaptive learning"""
    
    # Initial posting times for first 10-12 days
    INITIAL_POST_TIMES = ["09:00", "11:00", "14:00", "18:00", "20:00", "23:00"]
    
    def __init__(self, timezone_offset: int = 0):
        self.timezone_offset = timezone_offset
        self.adaptation_start_date = None
        self.initial_phase_days = 12
        self.tracking_data = {}
    
    def is_initial_phase(self) -> bool:
        """Check if still in initial 10-12 day phase"""
        try:
            if self.adaptation_start_date is None:
                return True
            
            days_elapsed = (datetime.now() - self.adaptation_start_date).days
            return days_elapsed < self.initial_phase_days
        
        except Exception as e:
            logger.error(f"Error checking phase: {e}")
            return True
    
    def get_initial_posting_schedule(self) -> List[datetime]:
        """Get initial posting times: 9 AM, 11 AM, 2 PM, 6 PM, 8 PM, 11 PM"""
        logger.info("Using initial posting schedule")
        
        today = datetime.now()
        posting_times = []
        
        for time_str in self.INITIAL_POST_TIMES:
            hour, minute = map(int, time_str.split(':'))
            post_time = today.replace(hour=hour, minute=minute, second=0)
            
            if post_time > datetime.now():
                posting_times.append(post_time)
        
        return posting_times
    
    def track_posting_performance(self, posting_time: datetime, 
                                 views: int, engagement_rate: float) -> bool:
        """Track performance of posting time slot"""
        try:
            hour = posting_time.hour
            
            if hour not in self.tracking_data:
                self.tracking_data[hour] = {'views': [], 'engagement': []}
            
            self.tracking_data[hour]['views'].append(views)
            self.tracking_data[hour]['engagement'].append(engagement_rate)
            
            logger.info(f"Tracked slot {hour}:00 - Views: {views}, Engagement: {engagement_rate:.2f}%")
            return True
        
        except Exception as e:
            logger.error(f"Error tracking performance: {e}")
            return False
    
    def analyze_posting_slot_performance(self) -> Dict:
        """Analyze which posting slots perform best"""
        try:
            logger.info("Analyzing posting slot performance...")
            
            slot_analysis = {}
            for hour, data in self.tracking_data.items():
                avg_views = sum(data['views']) / len(data['views']) if data['views'] else 0
                avg_engagement = sum(data['engagement']) / len(data['engagement']) if data['engagement'] else 0
                
                slot_analysis[f"{hour:02d}:00"] = {
                    'avg_views': avg_views,
                    'avg_engagement': avg_engagement,
                    'score': (avg_views * 0.6) + (avg_engagement * 0.4)
                }
            
            logger.info(f"Slot analysis: {slot_analysis}")
            return slot_analysis
        
        except Exception as e:
            logger.error(f"Error analyzing slots: {e}")
            return {}
    
    def get_optimal_posting_times(self) -> List[datetime]:
        """Get optimal posting times based on phase"""
        try:
            if self.is_initial_phase():
                logger.info("📅 Initial phase - using 9 AM, 11 AM, 2 PM, 6 PM, 8 PM, 11 PM")
                return self.get_initial_posting_schedule()
            else:
                logger.info("🚀 Optimization phase - using adaptive times")
                slot_performance = self.analyze_posting_slot_performance()
                return self._get_best_slots(slot_performance)
        
        except Exception as e:
            logger.error(f"Error getting optimal times: {e}")
            return self.get_initial_posting_schedule()
    
    def _get_best_slots(self, slot_analysis: Dict) -> List[datetime]:
        """Get best performing time slots"""
        try:
            sorted_slots = sorted(
                slot_analysis.items(),
                key=lambda x: x[1]['score'],
                reverse=True
            )
            
            best_slots = [slot[0] for slot in sorted_slots[:2]]
            logger.info(f"✨ Best performing slots: {best_slots}")
            
            today = datetime.now()
            posting_times = []
            
            for time_str in best_slots:
                hour, minute = map(int, time_str.split(':'))
                post_time = today.replace(hour=hour, minute=minute, second=0)
                
                if post_time > datetime.now():
                    posting_times.append(post_time)
            
            return posting_times
        
        except Exception as e:
            logger.error(f"Error getting best slots: {e}")
            return self.get_initial_posting_schedule()
    
    def calculate_optimal_post_time(self, category: str = 'news', 
                                    num_suggestions: int = 2) -> List[datetime]:
        """Calculate optimal posting times for daily videos"""
        logger.info(f"Calculating optimal times for {category}")
        
        try:
            optimal_times = self.get_optimal_posting_times()
            return optimal_times[:num_suggestions]
        
        except Exception as e:
            logger.error(f"Error calculating optimal time: {e}")
            return self.get_initial_posting_schedule()
    
    def batch_schedule_videos(self, 
                             video_ids: List[str],
                             category: str = 'general',
                             start_date: datetime = None) -> List[Tuple[str, datetime]]:
        """Schedule multiple videos with optimal spacing"""
        
        logger.info(f"Batch scheduling {len(video_ids)} videos")
        
        try:
            if start_date is None:
                start_date = datetime.now() + timedelta(days=1)
            
            scheduled_videos = []
            optimal_times = self.get_optimal_posting_times()
            
            for i, video_id in enumerate(video_ids):
                if i < len(optimal_times):
                    post_time = optimal_times[i]
                    scheduled_videos.append((video_id, post_time))
                    logger.info(f"Scheduled video {video_id} for {post_time}")
            
            return scheduled_videos
        
        except Exception as e:
            logger.error(f"Error in batch scheduling: {e}")
            return []
    
    def recommend_posting_strategy(self, 
                                  videos_per_day: int = 2,
                                  category: str = 'news') -> List[Tuple[str, datetime]]:
        """Recommend optimal posting strategy"""
        
        logger.info(f"Recommending posting strategy: {videos_per_day} videos/day")
        
        try:
            strategy = []
            optimal_times = self.get_optimal_posting_times()
            
            for i in range(min(videos_per_day, len(optimal_times))):
                post_time = optimal_times[i]
                engagement_score = self.get_engagement_score(post_time)
                strategy.append((f"Video_{i+1}", post_time, engagement_score))
            
            logger.info(f"Strategy: {strategy}")
            return strategy
        
        except Exception as e:
            logger.error(f"Error recommending strategy: {e}")
            return []
    
    def get_engagement_score(self, post_datetime: datetime) -> float:
        """Calculate engagement score for a specific datetime"""
        
        try:
            day_name = post_datetime.strftime('%A')
            hour = post_datetime.hour
            
            ENGAGEMENT_MATRIX = {
                'Monday': [2, 2, 1, 1, 1, 3, 4, 5, 6, 7, 8, 8, 7, 6, 7, 8, 9, 10, 9, 8, 7, 6, 5, 4],
                'Tuesday': [2, 2, 1, 1, 1, 3, 4, 5, 6, 7, 8, 8, 7, 6, 7, 8, 9, 10, 9, 8, 7, 6, 5, 4],
                'Wednesday': [2, 2, 1, 1, 1, 3, 4, 5, 6, 7, 8, 8, 7, 6, 7, 8, 9, 10, 9, 8, 7, 6, 5, 4],
                'Thursday': [2, 2, 1, 1, 1, 3, 4, 5, 6, 7, 8, 8, 7, 6, 7, 8, 9, 10, 9, 8, 7, 6, 5, 4],
                'Friday': [2, 2, 1, 1, 1, 3, 4, 5, 6, 7, 8, 8, 7, 6, 7, 8, 9, 11, 10, 9, 8, 7, 6, 5],
                'Saturday': [3, 3, 2, 2, 2, 4, 5, 6, 7, 8, 8, 8, 7, 6, 7, 8, 9, 10, 10, 9, 8, 7, 6, 5],
                'Sunday': [3, 3, 2, 2, 2, 4, 5, 6, 7, 8, 8, 8, 7, 6, 7, 8, 9, 10, 10, 9, 8, 7, 6, 5]
            }
            
            if day_name in ENGAGEMENT_MATRIX:
                engagement = ENGAGEMENT_MATRIX[day_name][hour]
                score = (engagement / 11) * 100
                return score
            
            return 50.0
        
        except Exception as e:
            logger.error(f"Error calculating engagement score: {e}")
            return 50.0
