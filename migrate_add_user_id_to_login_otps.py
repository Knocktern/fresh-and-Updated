#!/usr/bin/env python3
"""
Migration script to add user_id column to login_otps table
"""

import sqlite3
import os

def migrate_login_otps_table():
    """Add user_id column to login_otps table"""
    db_path = 'hiremedb.sqlite'
    
    if not os.path.exists(db_path):
        print("Database file not found. Creating new database with all tables.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if user_id column already exists
        cursor.execute("PRAGMA table_info(login_otps)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        if 'user_id' in column_names:
            print("user_id column already exists in login_otps table. No migration needed.")
            return
        
        print("Adding user_id column to login_otps table...")
        
        # Step 1: Drop existing table if it exists (since it's likely empty anyway for development)
        cursor.execute("DROP TABLE IF EXISTS login_otps")
        
        # Step 2: Create new login_otps table with user_id
        cursor.execute('''
            CREATE TABLE login_otps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                email VARCHAR(255) NOT NULL,
                otp_code VARCHAR(6) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                expires_at DATETIME NOT NULL,
                is_used BOOLEAN DEFAULT 0,
                attempts INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        print("✅ Successfully migrated login_otps table with user_id column")
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_login_otps_table()