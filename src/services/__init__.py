import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



from typing import List, Optional
from mysql.connector import Error
from config.db_config import DatabaseConfig
from models import User, Category, Quiz, Question, QuizResult

class UserService:
    @staticmethod
    def authenticate(username: str, password: str, role: str) -> Optional[User]:
        connection = DatabaseConfig.get_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(
                    "SELECT * FROM users WHERE username = %s AND password = %s AND role = %s",
                    (username, password, role)
                )
                result = cursor.fetchone()
                if result:
                    return User(**result)
                return None
            finally:
                cursor.close()
                connection.close()
        return None

    @staticmethod
    def register(username: str, password: str, role: str = 'candidate') -> bool:
        connection = DatabaseConfig.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                    (username, password, role)
                )
                connection.commit()
                return True
            except Error:
                return False
            finally:
                cursor.close()
                connection.close()
        return False

    @staticmethod
    def get_all_candidates() -> List[User]:
        connection = DatabaseConfig.get_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM users WHERE role = 'candidate'")
                return [User(**row) for row in cursor.fetchall()]
            finally:
                cursor.close()
                connection.close()
        return []

class CategoryService:
    @staticmethod
    def create(name: str, description: str) -> bool:
        connection = DatabaseConfig.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO quiz_categories (name, description) VALUES (%s, %s)",
                    (name, description)
                )
                connection.commit()
                return True
            finally:
                cursor.close()
                connection.close()
        return False

    @staticmethod
    def get_all() -> List[Category]:
        connection = DatabaseConfig.get_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM quiz_categories")
                return [Category(**row) for row in cursor.fetchall()]
            finally:
                cursor.close()
                connection.close()
        return []

class QuizService:
    @staticmethod
    def create(quiz: Quiz) -> bool:
        connection = DatabaseConfig.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    """INSERT INTO quizzes (category_id, title, description, time_limit)
                    VALUES (%s, %s, %s, %s)""",
                    (quiz.category_id, quiz.title, quiz.description, quiz.time_limit)
                )
                connection.commit()
                return True
            finally:
                cursor.close()
                connection.close()
        return False

    @staticmethod
    def get_by_category(category_id: int) -> List[Quiz]:
        connection = DatabaseConfig.get_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM quizzes WHERE category_id = %s", (category_id,))
                return [Quiz(**row) for row in cursor.fetchall()]
            finally:
                cursor.close()
                connection.close()
        return []

class QuestionService:
    @staticmethod
    def add_question(question: Question) -> bool:
        connection = DatabaseConfig.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    """INSERT INTO questions 
                    (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_answer)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (question.quiz_id, question.question_text, question.option_a,
                     question.option_b, question.option_c, question.option_d,
                     question.correct_answer)
                )
                connection.commit()
                return True
            finally:
                cursor.close()
                connection.close()
        return False

    @staticmethod
    def get_quiz_questions(quiz_id: int) -> List[Question]:
        connection = DatabaseConfig.get_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM questions WHERE quiz_id = %s", (quiz_id,))
                return [Question(**row) for row in cursor.fetchall()]
            finally:
                cursor.close()
                connection.close()
        return []

class QuizResultService:
    @staticmethod
    def save_result(result: QuizResult) -> bool:
        connection = DatabaseConfig.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    """INSERT INTO quiz_results (user_id, quiz_id, score, time_taken)
                    VALUES (%s, %s, %s, %s)""",
                    (result.user_id, result.quiz_id, result.score, result.time_taken)
                )
                connection.commit()
                return True
            finally:
                cursor.close()
                connection.close()
        return False

    @staticmethod
    def get_scoreboard(quiz_id: int) -> List[dict]:
        connection = DatabaseConfig.get_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("""
                    SELECT u.username, qr.score, qr.time_taken, qr.date_taken
                    FROM quiz_results qr
                    JOIN users u ON qr.user_id = u.id
                    WHERE qr.quiz_id = %s
                    ORDER BY qr.score DESC, qr.time_taken ASC
                """, (quiz_id,))
                return cursor.fetchall()
            finally:
                cursor.close()
                connection.close()
        return []