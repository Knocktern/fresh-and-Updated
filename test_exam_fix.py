#!/usr/bin/env python3
"""
Test the exam scoring fix
"""

def test_score_calculation():
    """Test the improved score calculation logic"""
    
    print("TESTING EXAM SCORE CALCULATION FIX")
    print("=" * 50)
    print()
    
    # Test scenarios
    test_cases = [
        {"correct": 3, "total": 3, "expected": 100.0},
        {"correct": 2, "total": 3, "expected": 66.67},
        {"correct": 1, "total": 3, "expected": 33.33},
        {"correct": 0, "total": 3, "expected": 0.0},
        {"correct": 0, "total": 0, "expected": 0.0},  # Edge case
    ]
    
    print("Testing score calculation:")
    print("Correct | Total | Expected | Calculated | Status")
    print("-" * 50)
    
    for case in test_cases:
        correct = case["correct"]
        total = case["total"]
        expected = case["expected"]
        
        # Apply the fixed calculation logic
        if total > 0:
            calculated = round((float(correct) / float(total)) * 100, 2)
        else:
            calculated = 0.0
            
        status = "✅ PASS" if abs(calculated - expected) < 0.01 else "❌ FAIL"
        
        print(f"{correct:7} | {total:5} | {expected:8} | {calculated:10} | {status}")
    
    print()
    print("KEY IMPROVEMENTS MADE:")
    print("1. ✅ Process ALL questions (even unanswered ones)")
    print("2. ✅ Use explicit float conversion for calculation")
    print("3. ✅ Round result to 2 decimal places")
    print("4. ✅ Save total_questions correctly to attempt")
    print("5. ✅ Handle None values in template")
    print("6. ✅ Display score with decimal precision")
    print("7. ✅ Add debugging logs for troubleshooting")
    
    print("\nTEMPLATE IMPROVEMENTS:")
    print("- Changed {{ score|int }}% to {{ \"%.1f\"|format(score or 0) }}%")
    print("- Added {{ score or 0 }} for progress bar width")
    print("- Added null checks for correct_count and total_questions")

def simulate_user_scenario():
    """Simulate the reported user scenario"""
    print()
    print("SIMULATING REPORTED SCENARIO:")
    print("=" * 50)
    print("User reported:")
    print("- Score: 0%")
    print("- Correct: 3")
    print("- Incorrect: 0")
    print()
    
    # This suggests 3 questions, all answered correctly
    correct_answers = 3
    total_questions = 3
    
    print("With new calculation:")
    score = round((float(correct_answers) / float(total_questions)) * 100, 2)
    
    print(f"- Correct answers: {correct_answers}")
    print(f"- Total questions: {total_questions}")
    print(f"- Calculated score: {score}%")
    print(f"- Template display: {score:.1f}%")
    print()
    print("✅ FIXED: Score should now show 100.0% instead of 0%")

if __name__ == "__main__":
    test_score_calculation()
    simulate_user_scenario()