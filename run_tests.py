"""
Test runner script
"""

import subprocess
import sys

def run_tests():
    """Run the test suite"""
    try:
        print("Running Task Manager API tests...")
        result = subprocess.run(['pytest', '-v'], capture_output=True, text=True)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("\n✅ All tests passed!")
        else:
            print("\n❌ Some tests failed!")
            sys.exit(1)
            
    except FileNotFoundError:
        print("❌ pytest not found. Please install it with: pip install pytest")
        sys.exit(1)

if __name__ == '__main__':
    run_tests()
