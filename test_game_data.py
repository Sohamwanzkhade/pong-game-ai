import pytest
import sqlite3
import os
import json
from datetime import datetime
from game_data import GameDataManager

@pytest.fixture
def test_db():
    """Create a temporary test database"""
    db_path = "test_game_stats.db"
    manager = GameDataManager(db_path)
    yield manager
    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)

class TestGameDataManager:
    """Test suite for GameDataManager class"""
    
    def test_database_creation(self, test_db):
        """Test that database is created successfully"""
        assert os.path.exists("test_game_stats.db")
        assert test_db.connection is not None
    
    def test_save_game_session(self, test_db):
        """Test saving a game session"""
        game_data = {
            'timestamp': datetime.now().isoformat(),
            'game_mode': 'ai',
            'player_score': 5,
            'opponent_score': 3,
            'ai_difficulty': 'normal',
            'ball_speed_multiplier': 1.0,
            'paddle_speed_multiplier': 1.0,
            'total_rallies': 25,
            'winner': 'player'
        }
        
        result = test_db.save_game_session(game_data)
        assert result is True
        
        # Verify data was saved
        cursor = test_db.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM game_sessions")
        count = cursor.fetchone()[0]
        assert count == 1
    
    def test_save_multiple_games(self, test_db):
        """Test saving multiple game sessions"""
        for i in range(5):
            game_data = {
                'timestamp': datetime.now().isoformat(),
                'game_mode': 'ai',
                'player_score': i + 1,
                'opponent_score': 5 - i,
                'ai_difficulty': 'normal',
                'ball_speed_multiplier': 1.0,
                'paddle_speed_multiplier': 1.0,
                'total_rallies': 20 + i,
                'winner': 'player' if (i + 1) > (5 - i) else 'opponent'
            }
            test_db.save_game_session(game_data)
        
        cursor = test_db.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM game_sessions")
        count = cursor.fetchone()[0]
        assert count == 5
    
    def test_get_player_stats(self, test_db):
        """Test retrieving player statistics"""
        # Add test data
        game_data = {
            'timestamp': datetime.now().isoformat(),
            'game_mode': 'ai',
            'player_score': 5,
            'opponent_score': 3,
            'ai_difficulty': 'normal',
            'ball_speed_multiplier': 1.0,
            'paddle_speed_multiplier': 1.0,
            'total_rallies': 25,
            'winner': 'player'
        }
        test_db.save_game_session(game_data)
        
        stats = test_db.get_player_stats()
        assert stats is not None
        assert 'total_games_played' in stats
        assert stats['total_games_played'] == 1
    
    def test_update_player_stats(self, test_db):
        """Test updating player statistics"""
        initial_stats = test_db.get_player_stats()
        
        # Add a win
        game_data = {
            'timestamp': datetime.now().isoformat(),
            'game_mode': 'ai',
            'player_score': 5,
            'opponent_score': 2,
            'ai_difficulty': 'normal',
            'ball_speed_multiplier': 1.0,
            'paddle_speed_multiplier': 1.0,
            'total_rallies': 20,
            'winner': 'player'
        }
        test_db.save_game_session(game_data)
        test_db.update_player_stats()
        
        updated_stats = test_db.get_player_stats()
        assert updated_stats['total_games_played'] > initial_stats['total_games_played']
    
    def test_export_to_json(self, test_db):
        """Test exporting data to JSON"""
        game_data = {
            'timestamp': datetime.now().isoformat(),
            'game_mode': 'ai',
            'player_score': 5,
            'opponent_score': 3,
            'ai_difficulty': 'normal',
            'ball_speed_multiplier': 1.0,
            'paddle_speed_multiplier': 1.0,
            'total_rallies': 25,
            'winner': 'player'
        }
        test_db.save_game_session(game_data)
        
        json_file = "test_export.json"
        test_db.export_to_json(json_file)
        
        assert os.path.exists(json_file)
        
        with open(json_file, 'r') as f:
            data = json.load(f)
            assert 'sessions' in data
            assert 'player_stats' in data
        
        # Cleanup
        os.remove(json_file)
    
    def test_get_recent_games(self, test_db):
        """Test retrieving recent games"""
        # Add multiple games
        for i in range(10):
            game_data = {
                'timestamp': datetime.now().isoformat(),
                'game_mode': 'ai',
                'player_score': i,
                'opponent_score': i + 1,
                'ai_difficulty': 'normal',
                'ball_speed_multiplier': 1.0,
                'paddle_speed_multiplier': 1.0,
                'total_rallies': 20,
                'winner': 'opponent'
            }
            test_db.save_game_session(game_data)
        
        recent = test_db.get_recent_games(limit=5)
        assert len(recent) <= 5
    
    def test_invalid_game_data(self, test_db):
        """Test handling of invalid game data"""
        invalid_data = {
            'timestamp': datetime.now().isoformat(),
            # Missing required fields
        }
        
        # Should handle gracefully or raise appropriate error
        with pytest.raises((KeyError, sqlite3.IntegrityError)):
            test_db.save_game_session(invalid_data)
    
    def test_database_persistence(self):
        """Test that data persists across connections"""
        db_path = "test_persistence.db"
        
        # First connection - save data
        manager1 = GameDataManager(db_path)
        game_data = {
            'timestamp': datetime.now().isoformat(),
            'game_mode': 'ai',
            'player_score': 5,
            'opponent_score': 3,
            'ai_difficulty': 'normal',
            'ball_speed_multiplier': 1.0,
            'paddle_speed_multiplier': 1.0,
            'total_rallies': 25,
            'winner': 'player'
        }
        manager1.save_game_session(game_data)
        manager1.close()
        
        # Second connection - verify data
        manager2 = GameDataManager(db_path)
        cursor = manager2.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM game_sessions")
        count = cursor.fetchone()[0]
        assert count == 1
        manager2.close()
        
        # Cleanup
        if os.path.exists(db_path):
            os.remove(db_path)

class TestGameDataEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_database_stats(self, test_db):
        """Test stats on empty database"""
        stats = test_db.get_player_stats()
        assert stats is not None
        assert stats['total_games_played'] == 0
        assert stats['total_wins'] == 0
        assert stats['total_losses'] == 0
    
    def test_high_scores(self, test_db):
        """Test handling of high scores"""
        game_data = {
            'timestamp': datetime.now().isoformat(),
            'game_mode': 'ai',
            'player_score': 999,
            'opponent_score': 998,
            'ai_difficulty': 'impossible',
            'ball_speed_multiplier': 2.5,
            'paddle_speed_multiplier': 2.0,
            'total_rallies': 1000,
            'winner': 'player'
        }
        result = test_db.save_game_session(game_data)
        assert result is True
    
    def test_same_score_draw(self, test_db):
        """Test handling of draw/tie games"""
        game_data = {
            'timestamp': datetime.now().isoformat(),
            'game_mode': 'ai',
            'player_score': 5,
            'opponent_score': 5,
            'ai_difficulty': 'normal',
            'ball_speed_multiplier': 1.0,
            'paddle_speed_multiplier': 1.0,
            'total_rallies': 25,
            'winner': 'draw'
        }
        result = test_db.save_game_session(game_data)
        assert result is True

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
