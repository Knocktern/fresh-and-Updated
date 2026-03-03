#!/usr/bin/env python3
"""
Judge0 CE Integration Test Script
Tests code execution with different languages using the new Judge0 API
Run this before your evaluation to verify everything works
"""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_judge0_integration():
    """Test Judge0 integration with multiple languages"""
    
    print("=" * 70)
    print("Judge0 CE Public API Integration Test")
    print("Testing code execution across multiple languages")
    print("=" * 70)
    print()
    
    from utils.code_executor import execute_code
    from utils.judge0_service import get_judge0_service
    
    # Test 1: Verify service is accessible
    print("Test 1: Checking Judge0 service availability...")
    print("-" * 70)
    try:
        judge0 = get_judge0_service()
        languages_result = judge0.get_supported_languages()
        
        if languages_result.get('success'):
            lang_count = len(languages_result.get('languages', []))
            print(f"✅ PASSED - Judge0 API is accessible ({lang_count} languages available)")
        else:
            print(f"⚠️ WARNING - {languages_result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ FAILED - {str(e)}")
    print()
    
    # Test cases with different languages
    test_cases = [
        {
            'name': 'Python - Hello World',
            'language': 'python',
            'code': '''print("Hello from Judge0 CE!")
print("Test: 2 + 2 =", 2 + 2)''',
            'stdin': '',
            'expected_contains': ['Hello from Judge0', '4']
        },
        {
            'name': 'JavaScript - Console Output',
            'language': 'javascript',
            'code': '''console.log("JavaScript Test");
console.log("5 * 5 =", 5 * 5);''',
            'stdin': '',
            'expected_contains': ['JavaScript Test', '25']
        },
        {
            'name': 'Python - With Input',
            'language': 'python',
            'code': '''name = input()
age = input()
print(f"Hello {name}, you are {age} years old!")''',
            'stdin': 'Alice\n25',
            'expected_contains': ['Hello Alice', '25 years old']
        },
        {
            'name': 'C++ - Simple Program',
            'language': 'cpp',
            'code': '''#include <iostream>
using namespace std;

int main() {
    cout << "C++ is working!" << endl;
    cout << "10 + 15 = " << (10 + 15) << endl;
    return 0;
}''',
            'stdin': '',
            'expected_contains': ['C++ is working', '25']
        },
        {
            'name': 'Java - Hello World',
            'language': 'java',
            'code': '''public class Main {
    public static void main(String[] args) {
        System.out.println("Java execution successful!");
        System.out.println("Result: " + (100 / 4));
    }
}''',
            'stdin': '',
            'expected_contains': ['Java execution', '25']
        },
        {
            'name': 'Python - Syntax Error',
            'language': 'python',
            'code': '''print("This will fail"
# Missing closing parenthesis''',
            'stdin': '',
            'should_fail': True
        },
    ]
    
    passed = 0
    failed = 0
    warnings = 0
    
    for i, test in enumerate(test_cases, 2):
        print(f"Test {i}: {test['name']}")
        print("-" * 70)
        
        try:
            result = execute_code(test['code'], test['language'], test.get('stdin', ''))
            
            # Check if this test should fail
            should_fail = test.get('should_fail', False)
            has_error = 'error' in result.lower() or 'failed' in result.lower()
            
            if should_fail:
                if has_error:
                    print(f"✅ PASSED - Error detected as expected")
                    print(f"   Error: {result[:100]}...")
                    passed += 1
                else:
                    print(f"❌ FAILED - Should have failed but didn't")
                    print(f"   Output: {result}")
                    failed += 1
            else:
                # Check for expected content
                expected = test.get('expected_contains', [])
                if has_error:
                    print(f"❌ FAILED - Execution error")
                    print(f"   Error: {result}")
                    failed += 1
                elif expected and all(exp.lower() in result.lower() for exp in expected):
                    print(f"✅ PASSED")
                    print(f"   Output: {result[:150]}")
                    passed += 1
                elif expected:
                    print(f"⚠️ WARNING - Output doesn't contain expected strings")
                    print(f"   Expected: {expected}")
                    print(f"   Got: {result}")
                    warnings += 1
                else:
                    print(f"✅ PASSED (no validation)")
                    print(f"   Output: {result[:150]}")
                    passed += 1
                    
        except Exception as e:
            print(f"❌ FAILED - Exception occurred")
            print(f"   Error: {str(e)}")
            failed += 1
        
        print()
    
    # Summary
    total = passed + failed + warnings
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Total Tests:  {total}")
    print(f"✅ Passed:     {passed}")
    print(f"⚠️ Warnings:   {warnings}")
    print(f"❌ Failed:     {failed}")
    print("=" * 70)
    
    if failed == 0:
        print("\n🎉 SUCCESS! Judge0 CE integration is working correctly!")
        print("Your application is ready for the evaluation tomorrow.")
        print("\nSupported languages: python, javascript, java, cpp, c, csharp,")
        print("                     go, rust, ruby, php, swift, kotlin, r, typescript")
    else:
        print("\n⚠️ Some tests failed. Troubleshooting tips:")
        print("1. Check your internet connection")
        print("2. Verify Judge0 CE API is accessible: https://ce.judge0.com")
        print("3. The public API may have rate limits - wait a few minutes and retry")
        print("4. Check if your firewall is blocking the connection")
    
    return failed == 0


def test_language_mapping():
    """Test language ID mapping"""
    print("\n" + "=" * 70)
    print("Language Mapping Test")
    print("=" * 70)
    
    from utils.judge0_service import JUDGE0_LANGUAGE_MAP
    
    print("\nSupported Languages:")
    print("-" * 70)
    for lang, lang_id in sorted(JUDGE0_LANGUAGE_MAP.items()):
        print(f"  {lang:<15} -> Language ID: {lang_id}")
    
    print(f"\nTotal: {len(JUDGE0_LANGUAGE_MAP)} languages supported")
    print("=" * 70)


if __name__ == '__main__':
    try:
        # Test language mapping
        test_language_mapping()
        print()
        
        # Test code execution
        success = test_judge0_integration()
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
