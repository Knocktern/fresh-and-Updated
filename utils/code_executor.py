"""
Code Executor Module
Provides code execution functionality using Judge0 CE public API
Replaces deprecated Piston API
"""

from utils.judge0_service import get_judge0_service

# Online execution configuration
ONLINE_EXECUTION_ENABLED = True


def execute_code_online(code, language, stdin=""):
    """
    Execute code using the Judge0 CE public API
    
    Args:
        code: Source code to execute
        language: Programming language (python, javascript, java, cpp, c, etc.)
        stdin: Standard input for the program (optional)
        
    Returns:
        String containing execution output or error message
    """
    try:
        if not ONLINE_EXECUTION_ENABLED:
            return "Online code execution is disabled."
        
        # Get Judge0 service instance
        judge0 = get_judge0_service()
        
        # Execute code
        result = judge0.execute_code(
            language=language,
            source_code=code,
            stdin=stdin,
            wait=True
        )
        
        # Return output or error
        if result.get('error'):
            return result['error']
        else:
            return result.get('output', '(No output)')
            
    except Exception as e:
        return f"Execution error: {str(e)}"


def execute_code(code, language, stdin=""):
    """
    Execute code via online Judge0 CE API
    
    Args:
        code: Source code to execute
        language: Programming language
        stdin: Standard input (optional)
        
    Returns:
        Execution output or error message
    """
    return execute_code_online(code, language, stdin)
