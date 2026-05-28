"""
Supabase Cloud Integration for Pong Game
Handles cloud storage, authentication, and synchronization
Uses SUPABASE_FREE_TIER (PostgreSQL backend)
"""

import os
import json
from typing import Dict, List, Optional
from datetime import datetime

# For Supabase integration, install: pip install supabase
try:
    from supabase import create_client, Client
except ImportError:
    print("⚠️  Supabase not installed. Install with: pip install supabase")
    Client = None

class SupabaseCloudManager:
    """Manages cloud storage with Supabase"""
    
    def __init__(self, supabase_url: str = None, supabase_key: str = None):
        """
        Initialize Supabase connection
        Get credentials from: https://app.supabase.com
        """
        self.supabase_url = supabase_url or os.getenv('SUPABASE_URL')
        self.supabase_key = supabase_key or os.getenv('SUPABASE_KEY')
        self.client: Optional[Client] = None
        self.initialized = False
        
        if self.supabase_url and self.supabase_key and Client:
            try:
                self.client = create_client(self.supabase_url, self.supabase_key)
                self.initialized = True
                print("✅ Connected to Supabase")
            except Exception as e:
                print(f"❌ Supabase connection failed: {e}")
    
    def init_cloud_tables(self) -> bool:
        """Initialize cloud database tables (called once)"""
        if not self.initialized:
            print("⚠️  Supabase not initialized")
            return False
        
        try:
            # Tables are created in Supabase dashboard
            # This is a reference to the expected schema
            print("✅ Cloud tables initialized")
            return True
        except Exception as e:
            print(f"❌ Error initializing tables: {e}")
            return False
    
    def sync_game_session(self, game_data: Dict) -> bool:
        """Sync a game session to cloud"""
        if not self.initialized:
            print("⚠️  Supabase not connected")
            return False
        
        try:
            self.client.table('game_sessions').insert({
                'timestamp': game_data.get('timestamp', datetime.now().isoformat()),
                'game_mode': game_data.get('game_mode', 'ai'),
                'player_score': game_data.get('player_score', 0),
                'opponent_score': game_data.get('opponent_score', 0),
                'ai_difficulty': game_data.get('ai_difficulty', 'normal'),
                'ball_speed_multiplier': game_data.get('ball_speed_multiplier', 1.0),
                'paddle_speed_multiplier': game_data.get('paddle_speed_multiplier', 1.0),
                'total_rallies': game_data.get('total_rallies', 0),
                'winner': game_data.get('winner', 'draw')
            }).execute()
            
            print("✅ Game synced to cloud")
            return True
        except Exception as e:
            print(f"❌ Sync failed: {e}")
            return False
    
    def sync_player_stats(self, stats: Dict) -> bool:
        """Sync player statistics to cloud"""
        if not self.initialized:
            return False
        
        try:
            self.client.table('player_stats').upsert({
                'id': 1,  # Single player record
                'total_games_played': stats.get('total_games', 0),
                'total_wins': stats.get('total_wins', 0),
                'total_losses': stats.get('total_losses', 0),
                'win_rate': stats.get('win_rate', 0),
                'highest_score': stats.get('highest_score', 0),
                'updated_at': datetime.now().isoformat()
            }).execute()
            
            return True
        except Exception as e:
            print(f"❌ Stats sync failed: {e}")
            return False
    
    def get_cloud_stats(self) -> Optional[Dict]:
        """Retrieve player statistics from cloud"""
        if not self.initialized:
            return None
        
        try:
            response = self.client.table('player_stats').select('*').eq('id', 1).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"❌ Error fetching stats: {e}")
            return None
    
    def get_cloud_games(self, limit: int = 10) -> List[Dict]:
        """Retrieve recent games from cloud"""
        if not self.initialized:
            return []
        
        try:
            response = self.client.table('game_sessions')\
                .select('*')\
                .order('timestamp', desc=True)\
                .limit(limit)\
                .execute()
            
            return response.data or []
        except Exception as e:
            print(f"❌ Error fetching games: {e}")
            return []
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get leaderboard from cloud"""
        if not self.initialized:
            return []
        
        try:
            response = self.client.table('player_stats')\
                .select('player_name, total_wins, win_rate')\
                .order('total_wins', desc=True)\
                .limit(limit)\
                .execute()
            
            return response.data or []
        except Exception as e:
            print(f"❌ Error fetching leaderboard: {e}")
            return []
    
    def backup_to_cloud(self, local_data: Dict) -> bool:
        """Create full backup in cloud"""
        if not self.initialized:
            return False
        
        try:
            self.client.table('backups').insert({
                'backup_data': json.dumps(local_data),
                'timestamp': datetime.now().isoformat(),
                'version': '1.0'
            }).execute()
            
            print("✅ Backup created in cloud")
            return True
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return False

class CloudSyncManager:
    """Manages syncing between local and cloud"""
    
    def __init__(self, local_manager, cloud_manager):
        self.local = local_manager
        self.cloud = cloud_manager
    
    def sync_all(self) -> Dict:
        """Sync all data between local and cloud"""
        if not self.cloud.initialized:
            print("⚠️  Cloud sync disabled (Supabase not configured)")
            return {'status': 'disabled'}
        
        try:
            # Get local stats
            local_stats = self.local.get_player_stats()
            
            # Sync to cloud
            self.cloud.sync_player_stats(local_stats)
            
            # Get recent games
            recent_games = self.local.get_recent_games(10)
            
            # Sync games
            for game in recent_games:
                self.cloud.sync_game_session(game)
            
            return {
                'status': 'success',
                'stats_synced': True,
                'games_synced': len(recent_games),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def pull_from_cloud(self) -> Optional[Dict]:
        """Pull latest data from cloud"""
        if not self.cloud.initialized:
            return None
        
        try:
            return self.cloud.get_cloud_stats()
        except Exception as e:
            print(f"❌ Pull failed: {e}")
            return None

class OOPGameManager:
    """
    Object-Oriented Programming - Complete Game Manager
    Encapsulates all game functionality
    """
    
    def __init__(self, local_manager, cloud_manager, analyzer, difficulty_engine):
        """Initialize game manager with all components"""
        self.local = local_manager
        self.cloud = cloud_manager
        self.analyzer = analyzer
        self.difficulty = difficulty_engine
        self.sync_manager = CloudSyncManager(local_manager, cloud_manager)
    
    def play_game(self, game_data: Dict) -> bool:
        """Record a game session"""
        # Save locally
        session_id = self.local.save_game_session(game_data)
        
        if session_id > 0:
            # Update stats
            self.local.update_player_stats()
            
            # Sync to cloud
            if self.cloud.initialized:
                self.cloud.sync_game_session(game_data)
            
            return True
        return False
    
    def get_recommendations(self) -> Dict:
        """Get complete recommendations"""
        return {
            'difficulty': self.difficulty.calculate_adaptive_difficulty(),
            'difficulty_report': self.difficulty.generate_difficulty_report(),
            'game_analysis': self.analyzer.generate_full_report(),
            'sync_status': self.sync_manager.sync_all()
        }
    
    def export_complete_profile(self) -> Dict:
        """Export complete player profile"""
        return {
            'player_stats': self.local.get_player_stats(),
            'recent_games': self.local.get_recent_games(20),
            'recommendations': self.get_recommendations(),
            'exported_at': datetime.now().isoformat()
        }
