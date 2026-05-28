"""
Pong Game - Main Data Analysis Script
Run this to analyze your game statistics and get recommendations
"""

from game_data import GameDataManager
from analyze_game import GameAnalyzer
from difficulty_engine import DynamicDifficultyEngine
import json
import sys

def main():
    """Main entry point for game analysis"""
    
    print("\n" + "="*60)
    print("🎮 PONG GAME DATA ANALYSIS SYSTEM")
    print("="*60)
    
    # Initialize data manager
    db_manager = GameDataManager('game_stats.db')
    
    # Initialize analyzer and difficulty engine
    analyzer = GameAnalyzer(db_manager)
    difficulty_engine = DynamicDifficultyEngine(db_manager, analyzer)
    
    while True:
        print("\n📋 MENU OPTIONS:")
        print("  1. 📊 View Player Stats & Analysis")
        print("  2. 🎯 View Difficulty Recommendations")
        print("  3. 🏆 View Recent Games")
        print("  4. 📈 View Performance Trend")
        print("  5. 💡 Get Training Suggestions")
        print("  6. 📥 Export All Data to JSON")
        print("  7. ➕ Add Sample Game Data (for testing)")
        print("  8. 🔄 Update Statistics")
        print("  9. ❌ Exit")
        
        choice = input("\nSelect option (1-9): ").strip()
        
        if choice == '1':
            view_player_stats(analyzer)
        elif choice == '2':
            view_difficulty_recommendations(difficulty_engine)
        elif choice == '3':
            view_recent_games(db_manager)
        elif choice == '4':
            view_performance_trend(db_manager)
        elif choice == '5':
            view_training_suggestions(difficulty_engine)
        elif choice == '6':
            export_data(db_manager)
        elif choice == '7':
            add_sample_data(db_manager)
        elif choice == '8':
            db_manager.update_player_stats()
            print("✅ Statistics updated successfully!")
        elif choice == '9':
            print("\n👋 Thanks for playing Pong! Goodbye!\n")
            db_manager.close()
            sys.exit(0)
        else:
            print("❌ Invalid option. Please try again.")

def view_player_stats(analyzer):
    """Display player statistics"""
    print("\n" + "="*60)
    print("📊 PLAYER STATISTICS")
    print("="*60)
    
    analyzer.print_report()

def view_difficulty_recommendations(difficulty_engine):
    """Display difficulty recommendations"""
    print("\n" + "="*60)
    print("🎯 DIFFICULTY ANALYSIS")
    print("="*60)
    
    difficulty_engine.print_difficulty_report()

def view_recent_games(db_manager):
    """Display recent games"""
    print("\n" + "="*60)
    print("🎮 RECENT GAMES")
    print("="*60)
    
    games = db_manager.get_recent_games(10)
    
    if not games:
        print("\nNo games played yet. Start playing to see your history!")
        return
    
    print(f"\nShowing {len(games)} most recent games:\n")
    for i, game in enumerate(games, 1):
        print(f"{i}. {game['timestamp']}")
        print(f"   Mode: {game['game_mode'].upper()}")
        print(f"   Score: You {game['player_score']} - {game['opponent_score']} Opponent")
        print(f"   Result: {'✅ WIN' if game['winner'] == 'player' else '❌ LOSS'}")
        print()

def view_performance_trend(db_manager):
    """Display performance trend"""
    print("\n" + "="*60)
    print("📈 PERFORMANCE TREND (Last 7 Days)")
    print("="*60)
    
    trend = db_manager.get_performance_trend(7)
    
    if not trend:
        print("\nNo data available yet.")
        return
    
    print()
    for date, data in sorted(trend.items()):
        win_rate = (data['wins'] / data['games_played'] * 100) if data['games_played'] > 0 else 0
        print(f"📅 {date}")
        print(f"   Games: {data['games_played']} | Wins: {data['wins']} | Losses: {data['losses']}")
        print(f"   Win Rate: {win_rate:.1f}%")
        print()

def view_training_suggestions(difficulty_engine):
    """Display training suggestions"""
    print("\n" + "="*60)
    print("💡 TRAINING SUGGESTIONS")
    print("="*60)
    
    training = difficulty_engine.suggest_training_focus()
    
    print(f"\n{training['focus_area']}")
    print(f"\n{training['suggestion']}\n")
    print("Tips:")
    for tip in training['tips']:
        print(f"  • {tip}")

def export_data(db_manager):
    """Export all data to JSON"""
    print("\n📥 EXPORTING DATA...")
    
    filename = input("Enter filename (default: game_stats.json): ").strip()
    if not filename:
        filename = "game_stats.json"
    
    if db_manager.export_stats_to_json(filename):
        print(f"✅ Data exported successfully to {filename}")
    else:
        print("❌ Error exporting data")

def add_sample_data(db_manager):
    """Add sample game data for testing"""
    print("\n" + "="*60)
    print("➕ ADDING SAMPLE DATA")
    print("="*60)
    
    sample_games = [
        {
            'timestamp': '2026-05-27T10:00:00',
            'game_mode': 'ai',
            'player_score': 5,
            'opponent_score': 3,
            'ai_difficulty': 'normal',
            'ball_speed_multiplier': 1.0,
            'paddle_speed_multiplier': 1.0,
            'total_rallies': 45,
            'winner': 'player',
            'duration_seconds': 180
        },
        {
            'timestamp': '2026-05-27T11:00:00',
            'game_mode': 'ai',
            'player_score': 3,
            'opponent_score': 5,
            'ai_difficulty': 'hard',
            'ball_speed_multiplier': 1.2,
            'paddle_speed_multiplier': 1.0,
            'total_rallies': 52,
            'winner': 'opponent',
            'duration_seconds': 220
        },
        {
            'timestamp': '2026-05-27T12:00:00',
            'game_mode': 'ai',
            'player_score': 6,
            'opponent_score': 2,
            'ai_difficulty': 'normal',
            'ball_speed_multiplier': 1.0,
            'paddle_speed_multiplier': 1.0,
            'total_rallies': 48,
            'winner': 'player',
            'duration_seconds': 195
        },
        {
            'timestamp': '2026-05-27T13:00:00',
            'game_mode': 'multiplayer',
            'player1_name': 'Player 1',
            'player2_name': 'Player 2',
            'player1_score': 7,
            'player2_score': 5,
            'winner': 'player1',
            'duration_seconds': 240
        },
        {
            'timestamp': '2026-05-27T14:00:00',
            'game_mode': 'ai',
            'player_score': 4,
            'opponent_score': 4,
            'ai_difficulty': 'normal',
            'ball_speed_multiplier': 1.0,
            'paddle_speed_multiplier': 1.0,
            'total_rallies': 50,
            'winner': 'draw',
            'duration_seconds': 210
        }
    ]
    
    for game in sample_games:
        if game['game_mode'] == 'ai':
            db_manager.save_game_session(game)
        else:
            db_manager.save_multiplayer_session(game)
    
    db_manager.update_player_stats()
    print(f"\n✅ Added {len(sample_games)} sample games!")
    print("You can now view statistics and recommendations.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)
