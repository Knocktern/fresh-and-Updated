"""
Judge0 CE Public API Service
Provides code execution functionality using Judge0 Community Edition public API
API Documentation: https://ce.judge0.com
"""

import requests
import time
from typing import Dict, Optional

# Judge0 CE Public API Configuration
JUDGE0_API_BASE = "https://ce.judge0.com"
REQUEST_TIMEOUT = 30  # seconds

# Language ID mapping for Judge0 CE
# Full list available at: https://ce.judge0.com/languages
JUDGE0_LANGUAGE_MAP = {
    'python': 71,       # Python (3.8.1)
    'javascript': 63,   # JavaScript (Node.js 12.14.0)
    'java': 62,         # Java (OpenJDK 13.0.1)
    'cpp': 54,          # C++ (GCC 9.2.0)
    'c': 50,            # C (GCC 9.2.0)
    'csharp': 51,       # C# (Mono 6.6.0.161)
    'go': 60,           # Go (1.13.5)
    'rust': 73,         # Rust (1.40.0)
    'ruby': 72,         # Ruby (2.7.0)
    'php': 68,          # PHP (7.4.1)
    'swift': 83,        # Swift (5.2.3)
    'kotlin': 78,       # Kotlin (1.3.70)
    'r': 80,            # R (4.0.0)
    'typescript': 74,   # TypeScript (3.7.4)
}


class Judge0Service:
    """Service class for interacting with Judge0 CE API"""
    
    def __init__(self, base_url: str = JUDGE0_API_BASE):
        """
        Initialize Judge0 service
        
        Args:
            base_url: Base URL for Judge0 API (default: public CE endpoint)
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
    
    def get_language_id(self, language: str) -> Optional[int]:
        """
        Get Judge0 language ID for a given language name
        
        Args:
            language: Language name (e.g., 'python', 'javascript')
            
        Returns:
            Language ID or None if not supported
        """
        return JUDGE0_LANGUAGE_MAP.get(language.lower())
    
    def get_supported_languages(self) -> Dict:
        """
        Fetch list of all supported languages from Judge0 API
        
        Returns:
            Dictionary of language information or error dict
        """
        try:
            response = self.session.get(
                f"{self.base_url}/languages",
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'languages': response.json()
                }
            else:
                return {
                    'success': False,
                    'error': f"Failed to fetch languages: {response.status_code}"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f"Network error: {str(e)}"
            }
    
    def execute_code(
        self,
        language: str,
        source_code: str,
        stdin: str = "",
        wait: bool = True
    ) -> Dict:
        """
        Execute code using Judge0 CE API
        
        Args:
            language: Programming language (e.g., 'python', 'javascript')
            source_code: Source code to execute
            stdin: Standard input for the program (optional)
            wait: If True, wait for execution to complete before returning
            
        Returns:
            Dictionary containing execution results:
            {
                'output': str,      # Program output
                'error': str,       # Error message if any
                'status': str,      # Execution status
                'executionTime': str,  # Execution time
                'memory': int       # Memory used in KB
            }
        """
        try:
            # Get language ID
            language_id = self.get_language_id(language)
            if language_id is None:
                return {
                    'output': '',
                    'error': f"Language '{language}' is not supported. Supported: {', '.join(JUDGE0_LANGUAGE_MAP.keys())}",
                    'status': 'Error',
                    'executionTime': '0s',
                    'memory': 0
                }
            
            # Prepare submission data
            submission_data = {
                'language_id': language_id,
                'source_code': source_code,
                'stdin': stdin
            }
            
            # Submit code for execution
            # Using wait=true for synchronous execution (simpler, blocks until done)
            submit_url = f"{self.base_url}/submissions"
            params = {
                'base64_encoded': 'false',
                'wait': 'true' if wait else 'false'
            }
            
            response = self.session.post(
                submit_url,
                json=submission_data,
                params=params,
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code not in [200, 201]:
                error_msg = self._extract_error_message(response)
                return {
                    'output': '',
                    'error': f"API Error: {error_msg}",
                    'status': 'Error',
                    'executionTime': '0s',
                    'memory': 0
                }
            
            result = response.json()
            
            # If wait=false, we need to poll for results
            if not wait:
                token = result.get('token')
                if not token:
                    return {
                        'output': '',
                        'error': 'No submission token received',
                        'status': 'Error',
                        'executionTime': '0s',
                        'memory': 0
                    }
                result = self._poll_submission(token)
            
            # Format and return results
            return self._format_result(result)
            
        except requests.exceptions.Timeout:
            return {
                'output': '',
                'error': 'Request timeout. Code execution took too long.',
                'status': 'Timeout',
                'executionTime': '0s',
                'memory': 0
            }
        except requests.exceptions.ConnectionError:
            return {
                'output': '',
                'error': 'Connection error. Unable to reach Judge0 API.',
                'status': 'Error',
                'executionTime': '0s',
                'memory': 0
            }
        except Exception as e:
            return {
                'output': '',
                'error': f'Execution error: {str(e)}',
                'status': 'Error',
                'executionTime': '0s',
                'memory': 0
            }
    
    def _poll_submission(self, token: str, max_attempts: int = 10) -> Dict:
        """
        Poll for submission results
        
        Args:
            token: Submission token
            max_attempts: Maximum number of polling attempts
            
        Returns:
            Submission result dictionary
        """
        for attempt in range(max_attempts):
            time.sleep(1)  # Wait 1 second between polls
            
            try:
                response = self.session.get(
                    f"{self.base_url}/submissions/{token}",
                    params={'base64_encoded': 'false'},
                    timeout=REQUEST_TIMEOUT
                )
                
                if response.status_code == 200:
                    result = response.json()
                    status_id = result.get('status', {}).get('id')
                    
                    # Status IDs: 1=In Queue, 2=Processing, 3+=Finished
                    if status_id and status_id > 2:
                        return result
                        
            except requests.exceptions.RequestException:
                continue
        
        # Timeout after max attempts
        return {
            'status': {'description': 'Timeout'},
            'stdout': None,
            'stderr': 'Execution timeout',
            'compile_output': None,
            'time': None,
            'memory': None
        }
    
    def _format_result(self, result: Dict) -> Dict:
        """
        Format Judge0 result into unified response format
        
        Args:
            result: Raw Judge0 API response
            
        Returns:
            Formatted result dictionary
        """
        status = result.get('status', {}).get('description', 'Unknown')
        stdout = result.get('stdout', '') or ''
        stderr = result.get('stderr', '') or ''
        compile_output = result.get('compile_output', '') or ''
        exec_time = result.get('time') or '0'
        memory = result.get('memory') or 0
        
        # Determine output and error
        output = ''
        error = ''
        
        # Check for compilation errors first
        if compile_output.strip():
            error = f"Compilation Error:\n{compile_output}"
            status = 'Compilation Error'
        # Check for runtime errors
        elif stderr.strip() and status != 'Accepted':
            error = f"Runtime Error:\n{stderr}"
        # Check for successful execution
        elif stdout.strip():
            output = stdout
        # No output case
        elif status == 'Accepted':
            output = '(No output)'
        else:
            # Other errors
            error = stderr if stderr.strip() else f"Status: {status}"
        
        # Format execution time
        try:
            time_float = float(exec_time)
            if time_float < 1:
                time_str = f"{int(time_float * 1000)}ms"
            else:
                time_str = f"{time_float:.2f}s"
        except (ValueError, TypeError):
            time_str = "0ms"
        
        return {
            'output': output,
            'error': error,
            'status': status,
            'executionTime': time_str,
            'memory': int(memory) if memory else 0
        }
    
    def _extract_error_message(self, response: requests.Response) -> str:
        """
        Extract error message from API response
        
        Args:
            response: HTTP response object
            
        Returns:
            Error message string
        """
        try:
            error_data = response.json()
            if isinstance(error_data, dict):
                return error_data.get('message', response.text)
            return str(error_data)
        except:
            return response.text or f"HTTP {response.status_code}"


# Singleton instance for easy import
_judge0_instance = None

def get_judge0_service() -> Judge0Service:
    """Get singleton instance of Judge0Service"""
    global _judge0_instance
    if _judge0_instance is None:
        _judge0_instance = Judge0Service()
    return _judge0_instance
