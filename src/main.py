import sys
import os

# Added parent directory to the system path as during importing, errors faced
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main.app import QuizApp
from config.db_config import DatabaseConfig

def main():
    
    DatabaseConfig.init_database()
    
    
    app = QuizApp()
    app.start()

if __name__ == "__main__":
    main()