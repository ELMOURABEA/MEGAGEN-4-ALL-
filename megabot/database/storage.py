"""
Database storage for research results and cache
"""
import sqlite3
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import os


class DatabaseStorage:
    """Manages persistent storage for MEGA-Bot"""
    
    def __init__(self, db_path: str = "megabot.db"):
        """
        Initialize database storage
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Research cache table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS research_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                platform TEXT NOT NULL,
                depth TEXT NOT NULL,
                results TEXT NOT NULL,
                timestamp REAL NOT NULL,
                UNIQUE(topic, platform, depth)
            )
        ''')
        
        # Query history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS query_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                platform TEXT NOT NULL,
                response TEXT NOT NULL,
                timestamp REAL NOT NULL
            )
        ''')
        
        # Document updates table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS document_updates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                update_type TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                date TEXT NOT NULL,
                timestamp REAL NOT NULL
            )
        ''')
        
        # Workflow tasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workflow_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT NOT NULL,
                status TEXT NOT NULL,
                priority INTEGER DEFAULT 1,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL,
                result TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def cache_research(self, topic: str, platform: str, depth: str, results: Dict[str, Any]):
        """Cache research results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO research_cache (topic, platform, depth, results, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (topic, platform, depth, json.dumps(results), datetime.now().timestamp()))
        
        conn.commit()
        conn.close()
    
    def get_cached_research(self, topic: str, platform: str, depth: str, max_age: float = 3600) -> Optional[Dict[str, Any]]:
        """Get cached research results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        current_time = datetime.now().timestamp()
        cursor.execute('''
            SELECT results, timestamp FROM research_cache
            WHERE topic = ? AND platform = ? AND depth = ? AND timestamp > ?
        ''', (topic, platform, depth, current_time - max_age))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return json.loads(row[0])
        return None
    
    def save_query(self, query: str, platform: str, response: str):
        """Save query to history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO query_history (query, platform, response, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (query, platform, response, datetime.now().timestamp()))
        
        conn.commit()
        conn.close()
    
    def get_query_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get query history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT query, platform, response, timestamp FROM query_history
            ORDER BY timestamp DESC LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "query": row[0],
                "platform": row[1],
                "response": row[2],
                "timestamp": row[3]
            }
            for row in rows
        ]
    
    def save_document_update(self, platform: str, update: Dict[str, Any]):
        """Save document update"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO document_updates (platform, update_type, title, description, date, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            platform,
            update.get("type", "update"),
            update.get("title", ""),
            update.get("description", ""),
            update.get("date", ""),
            datetime.now().timestamp()
        ))
        
        conn.commit()
        conn.close()
    
    def get_latest_updates(self, platform: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get latest document updates"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if platform:
            cursor.execute('''
                SELECT platform, update_type, title, description, date, timestamp
                FROM document_updates WHERE platform = ?
                ORDER BY timestamp DESC LIMIT ?
            ''', (platform, limit))
        else:
            cursor.execute('''
                SELECT platform, update_type, title, description, date, timestamp
                FROM document_updates
                ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "platform": row[0],
                "type": row[1],
                "title": row[2],
                "description": row[3],
                "date": row[4],
                "timestamp": row[5]
            }
            for row in rows
        ]
    
    def create_task(self, task_name: str, priority: int = 1) -> int:
        """Create a new workflow task"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now().timestamp()
        cursor.execute('''
            INSERT INTO workflow_tasks (task_name, status, priority, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (task_name, "pending", priority, timestamp, timestamp))
        
        task_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return task_id
    
    def update_task(self, task_id: int, status: str, result: Optional[str] = None):
        """Update task status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE workflow_tasks
            SET status = ?, result = ?, updated_at = ?
            WHERE id = ?
        ''', (status, result, datetime.now().timestamp(), task_id))
        
        conn.commit()
        conn.close()
    
    def get_pending_tasks(self) -> List[Dict[str, Any]]:
        """Get pending tasks"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, task_name, status, priority, created_at, updated_at
            FROM workflow_tasks WHERE status = 'pending'
            ORDER BY priority DESC, created_at ASC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": row[0],
                "task_name": row[1],
                "status": row[2],
                "priority": row[3],
                "created_at": row[4],
                "updated_at": row[5]
            }
            for row in rows
        ]
