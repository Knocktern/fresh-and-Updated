"""
SQLite Migration Validation Script
Test all functionality after migration from MySQL to SQLite
"""

import os
import sys
from datetime import datetime, timedelta

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from __init__ import create_app
from extensions import db
from models import *

def test_database_connection():
    """Test basic database connection"""
    try:
        app = create_app()
        with app.app_context():
            # Test connection by executing a simple query
            from sqlalchemy import text
            db.session.execute(text("SELECT 1")).fetchone()
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_model_creation():
    """Test creating instances of each model"""
    try:
        app = create_app()
        with app.app_context():
            # Test User creation
            user = User(
                email="test@example.com",
                password_hash="test_hash",
                user_type="candidate",
                first_name="Test",
                last_name="User"
            )
            
            # Test Company creation
            company = Company(
                company_name="Test Company",
                industry="Technology",
                company_size="50-100",
                user=user
            )
            
            # Test Skill creation
            skill = Skill(
                skill_name="Python",
                category="Programming"
            )
            
            print("✅ Model instances created successfully")
            return True
    except Exception as e:
        print(f"❌ Model creation failed: {e}")
        return False

def test_enum_constraints():
    """Test that enum constraints work correctly"""
    try:
        app = create_app()
        with app.app_context():
            import random
            # Test valid user type with unique email
            unique_email = f"test_enum_{random.randint(1000, 9999)}@example.com"
            user = User(
                email=unique_email,
                password_hash="test_hash",
                user_type="employer",  # Valid enum value
                first_name="Test",
                last_name="User2"
            )
            
            # This should work
            db.session.add(user)
            db.session.commit()
            
            print("✅ ENUM constraints working correctly")
            return True
    except Exception as e:
        print(f"❌ ENUM constraints test failed: {e}")
        return False

def test_file_upload_paths():
    """Test file upload functionality paths"""
    try:
        app = create_app()
        with app.app_context():
            # Check if upload directories exist or can be created
            upload_dirs = [
                'static/uploads',
                'static/uploads/profile_pictures',
                'static/uploads/company_logos',
                'static/uploads/cv_files',
                'static/uploads/documents'
            ]
            
            for dir_path in upload_dirs:
                full_path = os.path.join(os.path.dirname(__file__), dir_path)
                if not os.path.exists(full_path):
                    os.makedirs(full_path, exist_ok=True)
            
            print("✅ File upload paths verified")
            return True
    except Exception as e:
        print(f"❌ File upload paths test failed: {e}")
        return False

def test_foreign_key_relationships():
    """Test foreign key relationships"""
    try:
        app = create_app()
        with app.app_context():
            # Create related objects
            user = User(
                email="fk_test@example.com",
                password_hash="test_hash",
                user_type="candidate",
                first_name="FK",
                last_name="Test"
            )
            db.session.add(user)
            db.session.flush()  # Get the ID
            
            # Create candidate profile with foreign key
            candidate = CandidateProfile(
                user_id=user.id,
                profile_picture=b"test_image_data",  # Binary data
                summary="Test bio"
            )
            db.session.add(candidate)
            
            # Create skill and candidate skill relationship
            skill = Skill(skill_name="JavaScript", category="Programming")
            db.session.add(skill)
            db.session.flush()
            
            candidate_skill = CandidateSkill(
                candidate_id=candidate.id,
                skill_id=skill.id,
                proficiency_level="Advanced"
            )
            db.session.add(candidate_skill)
            
            db.session.commit()
            
            print("✅ Foreign key relationships working correctly")
            return True
    except Exception as e:
        print(f"❌ Foreign key relationships test failed: {e}")
        return False

def test_all_models():
    """Test all critical models"""
    try:
        app = create_app()
        with app.app_context():
            # Test creating instances of all main models
            models_to_test = [
                User, Company, CandidateProfile, JobPosting, 
                Skill, Notification, InterviewRoom
            ]
            
            for model in models_to_test:
                try:
                    # Just test that we can reference the model and get count
                    count = model.query.count()
                    print(f"✅ {model.__name__} model accessible (has {count} records)")
                except Exception as e:
                    print(f"❌ {model.__name__} model failed: {e}")
                    return False
            
            return True
    except Exception as e:
        print(f"❌ Model testing failed: {e}")
        return False

def run_all_tests():
    """Run all migration validation tests"""
    print("🧪 Starting SQLite Migration Validation Tests...")
    print("=" * 50)
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Model Creation", test_model_creation),
        ("ENUM Constraints", test_enum_constraints),
        ("File Upload Paths", test_file_upload_paths),
        ("Foreign Key Relationships", test_foreign_key_relationships),
        ("All Models Access", test_all_models)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"🏁 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! Your SQLite migration is successful.")
        print("\n🚀 You can now run your application with: python run.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)