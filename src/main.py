import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main.app import QuizApp
from config.db_config import DatabaseConfig

def main():
    # Initialize database
    DatabaseConfig.init_database()
    
    # Start the application
    app = QuizApp()
    app.start()

if __name__ == "__main__":
    main()