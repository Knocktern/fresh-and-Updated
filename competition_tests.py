"""
Complete Test Suite Runner
Runs all test categories for competition demo
"""

import time
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

try:
    from simple_tests import run_all_tests
    from api_tests import run_api_tests  
    from security_tests import run_security_tests
except ImportError:
    print("Error: Could not import test modules")
    sys.exit(1)

def run_competition_demo():
    """Run complete test suite for competition video"""
    start_time = time.time()
    
    print("HireMe Platform - Competition Test Demo")
    print("Testing all core functionality")
    print("=" * 50)
    print()
    
    # Track results
    test_results = []
    
    # Run core functionality tests
    print("Phase 1: Core Functionality Tests")
    print("-" * 30)
    core_result = run_all_tests()
    test_results.append(("Core Functionality", core_result))
    print()
    
    # Run API tests
    print("Phase 2: API Integration Tests")  
    print("-" * 30)
    api_result = run_api_tests()
    test_results.append(("API Integration", api_result))
    print()
    
    # Run security tests
    print("Phase 3: Security Validation Tests")
    print("-" * 30)
    security_result = run_security_tests()
    test_results.append(("Security Validation", security_result))
    print()
    
    # Final summary
    execution_time = time.time() - start_time
    
    print("=" * 50)
    print("COMPETITION DEMO SUMMARY")
    print("=" * 50)
    
    passed_phases = 0
    total_phases = len(test_results)
    
    for phase_name, result in test_results:
        status = "PASSED" if result else "FAILED"
        print(f"{phase_name}: {status}")
        if result:
            passed_phases += 1
    
    print()
    print(f"Overall Results: {passed_phases}/{total_phases} test phases passed")
    print(f"Execution Time: {execution_time:.1f} seconds")
    
    if passed_phases == total_phases:
        print("Platform Status: READY FOR PRODUCTION")
        print("All critical functionality validated")
    else:
        print("Platform Status: NEEDS ATTENTION")
        print("Some test phases require review")

def run_quick_demo():
    """Run a quick 30-second demo"""
    print("HireMe Platform - Quick Test Demo")
    print("=" * 35)
    print()
    
    # Run just core tests
    result = run_all_tests()
    
    if result:
        print("Quick Demo: ALL TESTS PASSED")
        print("Platform is functioning correctly")
    else:
        print("Quick Demo: SOME ISSUES FOUND")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        run_quick_demo()
    else:
        run_competition_demo()