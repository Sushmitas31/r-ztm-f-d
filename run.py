"""
Simple script to run the Flask application
"""

from app import create_app

if __name__ == '__main__':
    app = create_app()
    print("Starting Task Manager API...")
    print("API Documentation: http://localhost:5001/api/docs")
    print("API Base URL: http://localhost:5001/api")
    app.run(debug=True, host='0.0.0.0', port=5001)
