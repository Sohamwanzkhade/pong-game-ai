"""
Pong Game Data Analyzer
Analyzes game statistics and provides insights
"""

import json
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import statistics

class GameAnalyzer:
    """Analyzes game data and generates insights"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def get_win_loss_analysis(self) -> Dict:
        """Analyze win/loss patterns"""
        stats = self.data_manager.get_player_stats()
        
        if not stats or stats['total_games'] == 0:
            return {
                'total_games': 0,
                'wins': 0,
                'losses': 0,
                'win_percentage': 0,
                'status': 'No games played yet'
            }
        
        return {
            'total_games': stats['total_games'],
            'wins': stats['total_wins'],
            'losses': stats['total_losses'],
            'win_percentage': round(stats['win_rate'], 2),
            'status': self._get_performance_status(stats['win_rate'])
        }
    
    def get_score_analysis(self) -> Dict:
        """Analyze scoring patterns"""
        stats = self.data_manager.get_player_stats()
        
        if not stats or stats['total_games'] == 0:
            return {
                'average_score': 0,
                'highest_score': 0,
                'lowest_score': 0,
                'score_difference': 0
            }
        
        avg_score = stats['total_score'] / stats['total_games'] if stats['total_games'] > 0 else 0
        avg_opponent_score = stats['total_opponent_score'] / stats['total_games'] if stats['total_games'] > 0 else 0
        
        return {
            'average_score': round(avg_score, 2),
            'average_opponent_score': round(avg_opponent_score, 2),
            'highest_score': stats['highest_score'],
            'lowest_score': stats['lowest_score'],
            'score_difference': round(avg_score - avg_opponent_score, 2)
        }
    
    def get_rally_analysis(self) -> Dict:
        """Analyze rally patterns"""
        stats = self.data_manager.get_player_stats()
        
        return {
            'average_rally_length': round(stats.get('average_rally_length', 0), 2),
            'interpretation': 'Longer rallies indicate better rally control'
        }
    
    def get_difficulty_recommendation(self) -> Dict:
        """Recommend AI difficulty based on performance"""
        stats = self.data_manager.get_player_stats()
        
        if not stats or stats['total_games'] == 0:
            return {
                'current_difficulty': 'NORMAL',
                'recommended_difficulty': 'EASY',
                'reason': 'Start with Easy difficulty to learn the game'
            }
        
        win_rate = stats['win_rate']
        current_difficulty = stats.get('preferred_ai_difficulty', 'NORMAL')
        
        if win_rate > 60:
            return {
                'current_difficulty': current_difficulty,
                'recommended_difficulty': 'HARD',
                'reason': f'You win {win_rate:.1f}% of games. Try HARD difficulty!'
            }
        elif win_rate > 50:
            return {
                'current_difficulty': current_difficulty,
                'recommended_difficulty': 'HARD',
                'reason': f'You win {win_rate:.1f}% of games. Consider upgrading to HARD!'
            }
        elif win_rate < 30:
            return {
                'current_difficulty': current_difficulty,
                'recommended_difficulty': 'EASY',
                'reason': f'You win {win_rate:.1f}% of games. Try EASY difficulty to improve'
            }
        else:
            return {
                'current_difficulty': current_difficulty,
                'recommended_difficulty': 'NORMAL',
                'reason': f'Your {win_rate:.1f}% win rate matches NORMAL difficulty perfectly'
            }
    
    def get_settings_recommendation(self) -> Dict:
        """Recommend game settings based on preferences"""
        stats = self.data_manager.get_player_stats()
        
        return {
            'preferred_ball_speed': round(stats.get('preferred_ball_speed', 1.0), 2),
            'preferred_paddle_speed': round(stats.get('preferred_paddle_speed', 1.0), 2),
            'interpretation': 'These are your average settings from past games'
        }
    
    def get_progress_summary(self) -> Dict:
        """Get overall progress summary"""
        stats = self.data_manager.get_player_stats()
        performance = self.get_win_loss_analysis()
        difficulty = self.get_difficulty_recommendation()
        scores = self.get_score_analysis()
        
        return {
            'performance': performance,
            'scores': scores,
            'difficulty_recommendation': difficulty,
            'total_games_played': stats.get('total_games', 0),
            'skill_level': self._calculate_skill_level(performance['win_percentage']),
            'summary': self._get_progress_summary_text(stats, performance)
        }
    
    def _get_performance_status(self, win_rate: float) -> str:
        """Get performance status based on win rate"""
        if win_rate >= 70:
            return '🏆 Excellent'
        elif win_rate >= 60:
            return '⭐ Very Good'
        elif win_rate >= 50:
            return '✅ Good'
        elif win_rate >= 40:
            return '📈 Fair'
        else:
            return '💪 Keep Practicing'
    
    def _calculate_skill_level(self, win_rate: float) -> str:
        """Calculate skill level based on metrics"""
        if win_rate >= 70:
            return 'Expert'
        elif win_rate >= 60:
            return 'Advanced'
        elif win_rate >= 50:
            return 'Intermediate'
        elif win_rate >= 40:
            return 'Beginner'
        else:
            return 'Novice'
    
    def _get_progress_summary_text(self, stats: Dict, performance: Dict) -> str:
        """Generate progress summary text"""
        total = stats.get('total_games', 0)
        
        if total == 0:
            return "Start playing to see your progress!"
        elif total < 5:
            return "Keep playing more games to improve!"
        elif total < 20:
            return f"Good progress! You've played {total} games."
        else:
            return f"Excellent commitment! {total} games played. Keep improving!"
    
    def generate_full_report(self) -> Dict:
        """Generate complete analysis report"""
        self.data_manager.update_player_stats()
        
        return {
            'generated_at': datetime.now().isoformat(),
            'progress_summary': self.get_progress_summary(),
            'score_analysis': self.get_score_analysis(),
            'rally_analysis': self.get_rally_analysis(),
            'difficulty_recommendation': self.get_difficulty_recommendation(),
            'settings_recommendation': self.get_settings_recommendation(),
            'recent_games': self.data_manager.get_recent_games(5),
            'performance_trend': self.data_manager.get_performance_trend(7)
        }
    
    def print_report(self):
        """Print formatted analysis report"""
        report = self.generate_full_report()
        
        print("\n" + "="*60)
        print("🎮 PONG GAME ANALYSIS REPORT")
        print("="*60)
        
        summary = report['progress_summary']
        print(f"\n📊 PROGRESS SUMMARY")
        print(f"  Total Games: {summary['total_games_played']}")
        print(f"  Skill Level: {summary['skill_level']}")
        print(f"  Summary: {summary['summary']}")
        
        perf = report['progress_summary']['performance']
        print(f"\n🏆 PERFORMANCE")
        print(f"  Wins: {perf['wins']} | Losses: {perf['losses']}")
        print(f"  Win Rate: {perf['win_percentage']}%")
        print(f"  Status: {perf['status']}")
        
        scores = report['score_analysis']
        print(f"\n📈 SCORES")
        print(f"  Average Score: {scores['average_score']}")
        print(f"  Opponent Average: {scores['average_opponent_score']}")
        print(f"  Highest Score: {scores['highest_score']}")
        print(f"  Lowest Score: {scores['lowest_score']}")
        
        rally = report['rally_analysis']
        print(f"\n🎯 RALLIES")
        print(f"  Average Rally Length: {rally['average_rally_length']}")
        
        diff = report['difficulty_recommendation']
        print(f"\n🤖 AI DIFFICULTY")
        print(f"  Current: {diff['current_difficulty']}")
        print(f"  Recommended: {diff['recommended_difficulty']}")
        print(f"  Reason: {diff['reason']}")
        
        settings = report['settings_recommendation']
        print(f"\n⚙️ PREFERRED SETTINGS")
        print(f"  Ball Speed: {settings['preferred_ball_speed']}x")
        print(f"  Paddle Speed: {settings['preferred_paddle_speed']}x")
        
        print("\n" + "="*60)
        print("Generated:", report['generated_at'])
        print("="*60 + "\n")
