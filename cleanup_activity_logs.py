#!/usr/bin/env python3
"""
Script to clean up invalid activity log entries from the database
"""

import sqlite3
import os

def cleanup_invalid_activity_logs():
    """Remove activity logs with invalid operation types"""
    db_path = 'job_matching_system.db'
    
    if not os.path.exists(db_path):
        print(f"\n❌ Error: Database file '{db_path}' not found!")
        return
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='activity_logs'")
        if not cursor.fetchone():
            print("\n⚠️  Activity logs table doesn't exist yet.")
            print("This is normal if you haven't used the system much yet.")
            print("The table will be created automatically when needed.\n")
            conn.close()
            return
        
        # Check for invalid entries
        cursor.execute("""
            SELECT id, table_name, operation_type, user_id, timestamp 
            FROM activity_logs 
            WHERE operation_type NOT IN ('INSERT', 'UPDATE', 'DELETE', 'DOWNLOAD_CV')
        """)
        
        invalid_entries = cursor.fetchall()
        
        if not invalid_entries:
            print("✅ No invalid activity log entries found!")
            conn.close()
            return
        
        print(f"\n⚠️  Found {len(invalid_entries)} invalid activity log entries:")
        print("-" * 80)
        for entry in invalid_entries:
            print(f"ID: {entry[0]}, Table: {entry[1]}, Type: {entry[2]}, User: {entry[3]}, Time: {entry[4]}")
        print("-" * 80)
        
        # Delete invalid entries
        cursor.execute("""
            DELETE FROM activity_logs 
            WHERE operation_type NOT IN ('INSERT', 'UPDATE', 'DELETE', 'DOWNLOAD_CV')
        """)
        
        deleted_count = cursor.rowcount
        conn.commit()
        
        print(f"\n✅ Successfully removed {deleted_count} invalid activity log entries!")
        print("The admin dashboard should now work properly.\n")
        
    except sqlite3.Error as e:
        print(f"\n❌ Database error: {e}")
        conn.rollback()
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    try:
        cleanup_invalid_activity_logs()
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user.")
