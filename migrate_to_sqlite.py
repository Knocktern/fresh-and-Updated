"""
SQLite Migration Script - Enable Foreign Key Support
HireMe Platform Migration from MySQL to SQLite

This script ensures that SQLite foreign key constraints are enabled
and creates the database with proper schema.
"""

import sqlite3
import os

def setup_sqlite_foreign_keys():
    """Enable foreign key support for SQLite"""
    database_path = 'job_matching_system.db'
    
    # Connect to SQLite database
    conn = sqlite3.connect(database_path)
    
    # Enable foreign key constraints
    conn.execute('PRAGMA foreign_keys = ON')
    
    # Check if foreign keys are enabled
    result = conn.execute('PRAGMA foreign_keys').fetchone()
    if result[0] == 1:
        print("✅ Foreign key constraints are now enabled in SQLite")
    else:
        print("❌ Failed to enable foreign key constraints")
    
    conn.close()

def migrate_to_sqlite():
    """Create Flask app and initialize database"""
    # Import the app factory and db
    from __init__ import create_app
    from extensions import db
    
    app = create_app()
    
    with app.app_context():
        try:
            # Drop all tables if they exist (fresh migration)
            print("🗑️  Dropping existing tables...")
            db.drop_all()
            
            # Create all tables with new schema
            print("🏗️  Creating tables with SQLite schema...")
            db.create_all()
            
            print("✅ Database migration to SQLite completed successfully!")
            print(f"📍 Database location: {os.path.abspath('job_matching_system.db')}")
            
        except Exception as e:
            print(f"❌ Migration failed: {str(e)}")
            raise

if __name__ == '__main__':
    print("🚀 Starting migration from MySQL to SQLite...")
    
    # Import all models to ensure they're registered
    from models import *
    
    # Enable foreign keys
    setup_sqlite_foreign_keys()
    
    # Perform migration
    migrate_to_sqlite()
    
    print("🎉 Migration complete! Your application is now using SQLite.")
    print("\nNext steps:")
    print("1. Update any existing data if needed")
    print("2. Test all functionality")
    print("3. Run the application with: python run.py")