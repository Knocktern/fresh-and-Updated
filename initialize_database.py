#!/usr/bin/env python3
"""
Initialize database with all tables including updated LoginOTP model
"""

from run import create_app
from extensions import db
import os

def initialize_database():
    """Initialize the database with all tables"""
    app = create_app()
    
    with app.app_context():
        # Drop all existing tables to ensure clean state
        print("Dropping existing tables...")
        db.drop_all()
        
        # Create all tables
        print("Creating all tables...")
        db.create_all()
        
        print("✅ Database initialized successfully!")
        
        # Verify the login_otps table structure
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        
        if 'login_otps' in inspector.get_table_names():
            columns = inspector.get_columns('login_otps')
            print("\n📋 login_otps table structure:")
            for col in columns:
                print(f"  - {col['name']}: {col['type']}")
                
            if any(col['name'] == 'user_id' for col in columns):
                print("✅ user_id column exists in login_otps table")
            else:
                print("❌ user_id column missing from login_otps table")
        else:
            print("❌ login_otps table not found")

if __name__ == '__main__':
    initialize_database()