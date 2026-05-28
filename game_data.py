"""
Pong Game Data Manager
Handles all game data storage, retrieval, and analysis
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Tuple
import os

class GameDataManager:
    """Manages game statistics and data persistence"""
    
    def __init__(self, db_path: str = 'game_stats.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with required tables"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        # Create game sessions table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                game_mode TEXT NOT NULL,
                player_score INTEGER NOT NULL,
                opponent_score INTEGER NOT NULL,
                duration_seconds INTEGER,
                ai_difficulty TEXT,
                ball_speed_multiplier REAL,
                paddle_speed_multiplier REAL,
                total_rallies INTEGER,
                winner TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create player stats table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS player_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_games_played INTEGER DEFAULT 0,
                total_wins INTEGER DEFAULT 0,
                total_losses INTEGER DEFAULT 0,
                total_score INTEGER DEFAULT 0,
                total_opponent_score INTEGER DEFAULT 0,
                average_rally_length REAL DEFAULT 0,
                win_rate REAL DEFAULT 0,
                highest_score INTEGER DEFAULT 0,
                lowest_score INTEGER DEFAULT 0,
                preferred_ball_speed REAL DEFAULT 1.0,
                preferred_paddle_speed REAL DEFAULT 1.0,
                preferred_ai_difficulty TEXT DEFAULT 'normal',
                last_played TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create multiplayer stats table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS multiplayer_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player1_name TEXT DEFAULT 'Player 1',
                player2_name TEXT DEFAULT 'Player 2',
                player1_score INTEGER,
                player2_score INTEGER,
                winner TEXT,
                timestamp TEXT NOT NULL,
                duration_seconds INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create difficulty progression table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS difficulty_progression (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_session_id INTEGER,
                ai_difficulty TEXT,
                score_difference INTEGER,
                timestamp TEXT NOT NULL,
                FOREIGN KEY(game_session_id) REFERENCES game_sessions(id)
            )
        ''')
        
        self.conn.commit()
    
    def save_game_session(self, game_data: Dict) -> int:
        """Save a game session to database"""
        try:
            self.cursor.execute('''
                INSERT INTO game_sessions 
                (timestamp, game_mode, player_score, opponent_score, duration_seconds,
                 ai_difficulty, ball_speed_multiplier, paddle_speed_multiplier,
                 total_rallies, winner)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                game_data.get('timestamp', datetime.now().isoformat()),
                game_data.get('game_mode', 'ai'),
                game_data.get('player_score', 0),
                game_data.get('opponent_score', 0),
                game_data.get('duration_seconds', 0),
                game_data.get('ai_difficulty', 'normal'),
                game_data.get('ball_speed_multiplier', 1.0),
                game_data.get('paddle_speed_multiplier', 1.0),
                game_data.get('total_rallies', 0),
                game_data.get('winner', 'draw')
            ))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error saving game session: {e}")
            return -1
    
    def save_multiplayer_session(self, game_data: Dict) -> int:
        """Save a multiplayer game session"""
        try:
            self.cursor.execute('''
                INSERT INTO multiplayer_stats
                (player1_name, player2_name, player1_score, player2_score, winner, timestamp, duration_seconds)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                game_data.get('player1_name', 'Player 1'),
                game_data.get('player2_name', 'Player 2'),
                game_data.get('player1_score', 0),
                game_data.get('player2_score', 0),
                game_data.get('winner', 'draw'),
                game_data.get('timestamp', datetime.now().isoformat()),
                game_data.get('duration_seconds', 0)
            ))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error saving multiplayer session: {e}")
            return -1
    
    def update_player_stats(self):
        """Update aggregate player statistics"""
        try:
            self.cursor.execute('SELECT COUNT(*) FROM game_sessions WHERE game_mode = "ai"')
            total_games = self.cursor.fetchone()[0]
            
            self.cursor.execute('''
                SELECT COUNT(*) FROM game_sessions 
                WHERE game_mode = "ai" AND winner = "player"
            ''')
            total_wins = self.cursor.fetchone()[0]
            
            total_losses = total_games - total_wins
            
            self.cursor.execute('''
                SELECT SUM(player_score), SUM(opponent_score), AVG(total_rallies)
                FROM game_sessions WHERE game_mode = "ai"
            ''')
            result = self.cursor.fetchone()
            total_score = result[0] or 0
            total_opponent_score = result[1] or 0
            avg_rally = result[2] or 0
            
            win_rate = (total_wins / total_games * 100) if total_games > 0 else 0
            
            self.cursor.execute('''
                SELECT MAX(player_score), MIN(player_score)
                FROM game_sessions WHERE game_mode = "ai"
            ''')
            result = self.cursor.fetchone()
            highest = result[0] or 0
            lowest = result[1] or 0
            
            self.cursor.execute('''
                SELECT AVG(ball_speed_multiplier), AVG(paddle_speed_multiplier)
                FROM game_sessions WHERE game_mode = "ai"
            ''')
            result = self.cursor.fetchone()
            preferred_ball_speed = result[0] or 1.0
            preferred_paddle_speed = result[1] or 1.0
            
            self.cursor.execute('''
                DELETE FROM player_stats
            ''')
            
            self.cursor.execute('''
                INSERT INTO player_stats
                (total_games_played, total_wins, total_losses, total_score, total_opponent_score,
                 average_rally_length, win_rate, highest_score, lowest_score,
                 preferred_ball_speed, preferred_paddle_speed, last_played)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                total_games, total_wins, total_losses, total_score, total_opponent_score,
                avg_rally, win_rate, highest, lowest, preferred_ball_speed,
                preferred_paddle_speed, datetime.now().isoformat()
            ))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating player stats: {e}")
    
    def get_player_stats(self) -> Dict:
        """Retrieve all player statistics"""
        try:
            self.cursor.execute('SELECT * FROM player_stats')
            result = self.cursor.fetchone()
            
            if result:
                return {
                    'total_games': result[1],
                    'total_wins': result[2],
                    'total_losses': result[3],
                    'total_score': result[4],
                    'total_opponent_score': result[5],
                    'average_rally_length': result[6],
                    'win_rate': result[7],
                    'highest_score': result[8],
                    'lowest_score': result[9],
                    'preferred_ball_speed': result[10],
                    'preferred_paddle_speed': result[11],
                    'preferred_ai_difficulty': result[12]
                }
            return {}
        except sqlite3.Error as e:
            print(f"Error retrieving player stats: {e}")
            return {}
    
    def get_recent_games(self, limit: int = 10) -> List[Dict]:
        """Get recent game sessions"""
        try:
            self.cursor.execute('''
                SELECT id, timestamp, game_mode, player_score, opponent_score, winner
                FROM game_sessions
                ORDER BY created_at DESC
                LIMIT ?
            ''', (limit,))
            
            games = []
            for row in self.cursor.fetchall():
                games.append({
                    'id': row[0],
                    'timestamp': row[1],
                    'game_mode': row[2],
                    'player_score': row[3],
                    'opponent_score': row[4],
                    'winner': row[5]
                })
            return games
        except sqlite3.Error as e:
            print(f"Error retrieving recent games: {e}")
            return []
    
    def get_performance_trend(self, days: int = 7) -> Dict:
        """Get performance trend over specified days"""
        try:
            self.cursor.execute(f'''
                SELECT DATE(created_at), COUNT(*), SUM(CASE WHEN winner = "player" THEN 1 ELSE 0 END)
                FROM game_sessions
                WHERE game_mode = "ai" AND created_at >= datetime('now', '-{days} days')
                GROUP BY DATE(created_at)
                ORDER BY DATE(created_at)
            ''')
            
            trend = {}
            for row in self.cursor.fetchall():
                trend[row[0]] = {
                    'games_played': row[1],
                    'wins': row[2] or 0,
                    'losses': (row[1] - (row[2] or 0))
                }
            return trend
        except sqlite3.Error as e:
            print(f"Error retrieving performance trend: {e}")
            return {}
    
    def export_stats_to_json(self, filename: str = 'game_stats.json') -> bool:
        """Export all statistics to JSON file"""
        try:
            stats = {
                'player_stats': self.get_player_stats(),
                'recent_games': self.get_recent_games(20),
                'performance_trend': self.get_performance_trend(30),
                'exported_at': datetime.now().isoformat()
            }
            
            with open(filename, 'w') as f:
                json.dump(stats, f, indent=2)
            
            print(f"Stats exported to {filename}")
            return True
        except Exception as e:
            print(f"Error exporting stats: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def __del__(self):
        """Destructor to ensure connection is closed"""
        self.close()
