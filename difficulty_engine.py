"""
Pong Game Dynamic Difficulty Engine
Adapts AI difficulty based on player performance history
"""

from typing import Dict, List
from datetime import datetime, timedelta

class DynamicDifficultyEngine:
    """Manages dynamic difficulty adjustment based on performance"""
    
    def __init__(self, data_manager, analyzer):
        self.data_manager = data_manager
        self.analyzer = analyzer
    
    def calculate_adaptive_difficulty(self) -> str:
        """Calculate recommended difficulty based on complete history"""
        stats = self.data_manager.get_player_stats()
        
        if not stats or stats['total_games'] == 0:
            return 'easy'  # Start new players on easy
        
        win_rate = stats.get('win_rate', 0)
        total_games = stats.get('total_games', 0)
        
        # Determine difficulty based on win rate
        if win_rate >= 75:
            return 'impossible'
        elif win_rate >= 65:
            return 'hard'
        elif win_rate >= 45:
            return 'normal'
        elif win_rate >= 30:
            return 'easy'
        else:
            return 'easy'
    
    def get_difficulty_progression(self) -> Dict:
        """Get difficulty progression over time"""
        self.data_manager.update_player_stats()
        stats = self.data_manager.get_player_stats()
        
        progression = {
            'current_difficulty': self.calculate_adaptive_difficulty(),
            'win_rate': round(stats.get('win_rate', 0), 2),
            'total_games': stats.get('total_games', 0),
            'progression_path': self._get_progression_path(stats),
            'next_milestone': self._get_next_milestone(stats)
        }
        
        return progression
    
    def get_customized_ai_params(self) -> Dict:
        """Get customized AI parameters based on player history"""
        stats = self.data_manager.get_player_stats()
        difficulty = self.calculate_adaptive_difficulty()
        
        # AI behavior parameters
        difficulty_params = {
            'easy': {
                'ai_speed': 3,
                'reaction_time': 200,  # ms
                'miss_rate': 0.35,
                'accuracy': 0.65
            },
            'normal': {
                'ai_speed': 5,
                'reaction_time': 100,
                'miss_rate': 0.0,
                'accuracy': 0.85
            },
            'hard': {
                'ai_speed': 6,
                'reaction_time': 50,
                'miss_rate': 0.0,
                'accuracy': 0.95
            },
            'impossible': {
                'ai_speed': 7,
                'reaction_time': 20,
                'miss_rate': 0.0,
                'accuracy': 1.0
            }
        }
        
        params = difficulty_params.get(difficulty, difficulty_params['normal'])
        params['difficulty_level'] = difficulty.upper()
        params['recommended_for_win_rate'] = round(stats.get('win_rate', 0), 2)
        
        return params
    
    def _get_progression_path(self, stats: Dict) -> List[str]:
        """Get the difficulty progression path the player should follow"""
        win_rate = stats.get('win_rate', 0)
        total_games = stats.get('total_games', 0)
        
        path = ['EASY', 'NORMAL', 'HARD', 'IMPOSSIBLE']
        
        if total_games == 0:
            return path
        
        current_index = max(0, min(3, int(win_rate / 25)))
        return path[current_index:]
    
    def _get_next_milestone(self, stats: Dict) -> Dict:
        """Get next achievement milestone"""
        total_games = stats.get('total_games', 0)
        win_rate = stats.get('win_rate', 0)
        wins = stats.get('total_wins', 0)
        
        milestones = [
            {'games': 10, 'name': '🎮 10 Games Played', 'progress': min(100, (total_games / 10) * 100)},
            {'games': 50, 'name': '🏆 50 Games Played', 'progress': min(100, (total_games / 50) * 100)},
            {'games': 100, 'name': '⭐ 100 Games Played', 'progress': min(100, (total_games / 100) * 100)},
            {'wins': 25, 'name': '🎯 25 Wins', 'progress': min(100, (wins / 25) * 100)},
            {'wins': 50, 'name': '👑 50 Wins', 'progress': min(100, (wins / 50) * 100)},
            {'rate': 60, 'name': '📈 60% Win Rate', 'progress': min(100, (win_rate / 60) * 100)},
            {'rate': 75, 'name': '🏅 75% Win Rate', 'progress': min(100, (win_rate / 75) * 100)},
        ]
        
        # Find next uncompleted milestone
        for milestone in milestones:
            if milestone['progress'] < 100:
                return {
                    'name': milestone['name'],
                    'progress': round(milestone['progress'], 1),
                    'description': f"{round(milestone['progress'], 1)}% complete"
                }
        
        return {
            'name': '🌟 Master Player',
            'progress': 100,
            'description': 'You have achieved mastery!'
        }
    
    def suggest_training_focus(self) -> Dict:
        """Suggest areas for improvement"""
        stats = self.data_manager.get_player_stats()
        
        if not stats or stats['total_games'] == 0:
            return {
                'focus_area': 'Learn Basics',
                'suggestion': 'Play against EASY AI to understand game mechanics',
                'tips': ['Move mouse smoothly', 'Use arrow keys for backup control', 'Keep paddle centered']
            }
        
        avg_rally = stats.get('average_rally_length', 0)
        win_rate = stats.get('win_rate', 0)
        score_diff = (stats.get('total_score', 0) - stats.get('total_opponent_score', 0)) / stats.get('total_games', 1)
        
        if avg_rally < 5:
            return {
                'focus_area': '🎯 Improve Rally Control',
                'suggestion': 'Your rallies are short. Focus on defensive play.',
                'tips': ['Anticipate ball direction', 'Position paddle early', 'Use spin technique (hit edge)']
            }
        elif win_rate < 40:
            return {
                'focus_area': '💪 Scoring Strategy',
                'suggestion': 'You lose more than you win. Practice aggressive play.',
                'tips': ['Hit balls at angles', 'Move to edges for better angles', 'React faster to AI shots']
            }
        elif win_rate < 60:
            return {
                'focus_area': '📈 Consistency',
                'suggestion': 'Good progress! Focus on consistent winning.',
                'tips': ['Maintain paddle center', 'Smooth movements', 'Practice specific AI difficulties']
            }
        else:
            return {
                'focus_area': '🏆 Advanced Techniques',
                'suggestion': 'You are skilled! Try harder difficulties.',
                'tips': ['Master HARD/IMPOSSIBLE modes', 'Optimize reaction time', 'Study AI patterns']
            }
    
    def generate_difficulty_report(self) -> Dict:
        """Generate complete difficulty analysis report"""
        return {
            'adaptive_difficulty': self.calculate_adaptive_difficulty(),
            'progression': self.get_difficulty_progression(),
            'ai_parameters': self.get_customized_ai_params(),
            'next_milestone': self._get_next_milestone(self.data_manager.get_player_stats()),
            'training_focus': self.suggest_training_focus(),
            'generated_at': datetime.now().isoformat()
        }
    
    def print_difficulty_report(self):
        """Print formatted difficulty report"""
        report = self.generate_difficulty_report()
        
        print("\n" + "="*60)
        print("🎯 DYNAMIC DIFFICULTY ANALYSIS")
        print("="*60)
        
        prog = report['progression']
        print(f"\n📊 PROGRESSION STATUS")
        print(f"  Current Difficulty: {prog['current_difficulty'].upper()}")
        print(f"  Win Rate: {prog['win_rate']}%")
        print(f"  Total Games: {prog['total_games']}")
        print(f"  Path: {' → '.join(prog['progression_path'])}")
        
        ai = report['ai_parameters']
        print(f"\n🤖 AI PARAMETERS FOR {ai['difficulty_level']}")
        print(f"  AI Speed: {ai['ai_speed']}")
        print(f"  Reaction Time: {ai['reaction_time']}ms")
        print(f"  Miss Rate: {ai['miss_rate']*100:.0f}%")
        print(f"  Accuracy: {ai['accuracy']*100:.0f}%")
        
        milestone = report['next_milestone']
        print(f"\n🏅 NEXT MILESTONE")
        print(f"  {milestone['name']}")
        print(f"  Progress: {milestone['progress']}%")
        print(f"  {milestone['description']}")
        
        training = report['training_focus']
        print(f"\n💡 TRAINING FOCUS: {training['focus_area']}")
        print(f"  {training['suggestion']}")
        print(f"  Tips:")
        for tip in training['tips']:
            print(f"    • {tip}")
        
        print("\n" + "="*60)
        print("Generated:", report['generated_at'])
        print("="*60 + "\n")
