import sys
import os

# Added parent directory to the system path as during importing errors faced
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from typing import Optional, Tuple
from models import Quiz, QuizResult
from config.db_config import DatabaseConfig



class QuizService:
    @staticmethod
    def start_quiz(quiz_id: int, user_id: int) -> Optional[Tuple[int, float]]:
        """
        Start a quiz and return the score and time taken
        Returns: Tuple of (score, time_taken_in_seconds) or None if error
        """
        start_time = time.time()
        score = 0
        # ... existing quiz logic ...
        
        # Calculate actual time taken in seconds
        end_time = time.time()
        time_taken = round(end_time - start_time)
        
        # Save quiz result
        connection = DatabaseConfig.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    """INSERT INTO quiz_results 
                       (user_id, quiz_id, score, time_taken, date_taken) 
                       VALUES (%s, %s, %s, %s, NOW())""",
                    (user_id, quiz_id, score, time_taken)
                )
                connection.commit()
                return score, time_taken
            finally:
                cursor.close()
                connection.close()
        return None