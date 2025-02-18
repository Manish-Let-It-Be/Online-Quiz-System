import sys
import os

# Added parent directory to the system path as during importing errors faced
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List
from mysql.connector import Error
from config.db_config import DatabaseConfig
from helper import ConsoleHelper

class DatabaseService:
    @staticmethod
    def reset_database() -> bool:
        """Resets all tables in the database by truncating them in the correct order."""
        # Order matters due to foreign key constraints
        tables = [
            'quiz_results',
            'questions',
            'quizzes',
            'quiz_categories',
            'users'
        ]
        
        connection = DatabaseConfig.get_connection()
        if connection:
            try:
                cursor = connection.cursor()

                cursor.execute("SHOW TABLES")
                existing_tables = [table[0] for table in cursor.fetchall()]
                
                # Temporarily disable foreign key checks
                cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
                
                for table in tables:
                    if table in existing_tables:
                        cursor.execute(f"TRUNCATE TABLE {table}")
                
                # Re-enable foreign key checks
                cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
                
                connection.commit()
                return True
            except Error as e:
                print(f"Error resetting database: {e}")
                return False
            finally:
                cursor.close()
                connection.close()
        return False